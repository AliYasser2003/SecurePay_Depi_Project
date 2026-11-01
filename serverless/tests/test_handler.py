import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from handler import lambda_handler


def make_event(method="POST", body=None, groups=None):
    event = {
        "httpMethod": method,
        "body": json.dumps(body) if body is not None else None,
    }

    # Simulate Cognito claims supplied by API Gateway's authorizer.
    if groups is not None:
        event["requestContext"] = {
            "authorizer": {
                "claims": {
                    "cognito:groups": groups,
                }
            }
        }

    return event


def test_valid_payment_request():
    result = lambda_handler(
        make_event(body={"amount": 25.50, "currency": "USD"},
                   groups=["customers"]), None
    )

    assert result["statusCode"] == 201
    assert json.loads(result["body"])["simulated"] is True


def test_reject_zero_amount():
    result = lambda_handler(
        make_event(body={"amount": 0, "currency": "USD"},
                   groups=["customers"]), None
    )
    assert result["statusCode"] == 400


def test_reject_negative_amount():
    result = lambda_handler(
        make_event(body={"amount": -5, "currency": "USD"},
                   groups=["customers"]), None
    )
    assert result["statusCode"] == 400


def test_reject_invalid_currency():
    result = lambda_handler(
        make_event(body={"amount": 25, "currency": "usd"},
                   groups=["customers"]), None
    )
    assert result["statusCode"] == 400


def test_reject_wrong_http_method():
    result = lambda_handler(make_event(method="GET"), None)
    assert result["statusCode"] == 405


def test_reject_invalid_json():
    result = lambda_handler(
        {
            "httpMethod": "POST",
            "body": "not-json",
            "requestContext": {
                "authorizer": {
                    "claims": {"cognito:groups": ["customers"]}
                }
            },
        },
        None,
    )
    assert result["statusCode"] == 400


def test_reject_missing_amount():
    result = lambda_handler(
        make_event(body={"currency": "USD"}, groups=["customers"]), None
    )
    assert result["statusCode"] == 400


def test_reject_boolean_amount():
    result = lambda_handler(
        make_event(body={"amount": True, "currency": "USD"},
                   groups=["customers"]), None
    )
    assert result["statusCode"] == 400


def test_reject_amount_above_limit():
    result = lambda_handler(
        make_event(body={"amount": 1000001, "currency": "USD"},
                   groups=["customers"]), None
    )
    assert result["statusCode"] == 400


def test_reject_non_object_json():
    event = {
        "httpMethod": "POST",
        "body": json.dumps([{"amount": 25, "currency": "USD"}]),
        "requestContext": {
            "authorizer": {
                "claims": {"cognito:groups": ["customers"]}
            }
        },
    }
    result = lambda_handler(event, None)
    assert result["statusCode"] == 400


def test_reject_missing_currency():
    result = lambda_handler(
        make_event(body={"amount": 25}, groups=["customers"]), None
    )
    assert result["statusCode"] == 400


def test_response_has_security_headers():
    result = lambda_handler(
        make_event(body={"amount": 25, "currency": "USD"},
                   groups=["customers"]), None
    )
    assert result["headers"]["X-Content-Type-Options"] == "nosniff"
    assert result["headers"]["Cache-Control"] == "no-store"


def test_reject_user_without_authorized_group():
    result = lambda_handler(
        make_event(
            body={"amount": 25, "currency": "USD"},
            groups=["other"],
        ),
        None,
    )
    assert result["statusCode"] == 403


def test_reject_missing_group_claims():
    result = lambda_handler(
        make_event(body={"amount": 25, "currency": "USD"}),
        None,
    )
    assert result["statusCode"] == 403


def test_admin_can_submit_payment():
    result = lambda_handler(
        make_event(
            body={"amount": 25, "currency": "USD"},
            groups=["admins"],
        ),
        None,
    )
    assert result["statusCode"] == 201
