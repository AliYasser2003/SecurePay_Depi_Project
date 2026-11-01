import json
import re
from decimal import Decimal, InvalidOperation


def response(status_code: int, body: dict) -> dict:
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "X-Content-Type-Options": "nosniff",
            "Cache-Control": "no-store",
        },
        "body": json.dumps(body),
    }


def lambda_handler(event, context):
    if event.get("httpMethod") != "POST":
        return response(405, {"error": "Method not allowed"})

    # RBAC: read Cognito groups from API Gateway's verified authorizer claims.
    claims = (
        event.get("requestContext", {})
        .get("authorizer", {})
        .get("claims", {})
    )
    groups_claim = claims.get("cognito:groups", [])

    if isinstance(groups_claim, str):
        try:
            groups = set(json.loads(groups_claim))
        except (json.JSONDecodeError, TypeError):
            groups = {g.strip() for g in groups_claim.split(",") if g.strip()}
    elif isinstance(groups_claim, list):
        groups = set(groups_claim)
    else:
        groups = set()

    if "customers" not in groups and "admins" not in groups:
        return response(403, {"error": "User is not assigned to an authorized group"})

    try:
        body = json.loads(event.get("body") or "")
    except (json.JSONDecodeError, TypeError):
        return response(400, {"error": "Invalid JSON body"})

    if not isinstance(body, dict):
        return response(400, {"error": "Request body must be a JSON object"})

    amount = body.get("amount")
    currency = body.get("currency")

    if isinstance(amount, bool) or amount is None:
        return response(400, {"error": "Amount must be a positive number"})

    try:
        value = Decimal(str(amount))
    except (InvalidOperation, ValueError):
        return response(400, {"error": "Amount must be a positive number"})

    if not value.is_finite() or value <= 0 or value > Decimal("1000000"):
        return response(400, {"error": "Amount is outside the allowed range"})

    if not isinstance(currency, str) or not re.fullmatch(
        r"[A-Z]{3}", currency
    ):
        return response(400, {"error": "Currency must be a 3-letter uppercase code"})

    return response(
        201,
        {
            "message": "Payment request accepted for simulation",
            "amount": str(value),
            "currency": currency,
            "simulated": True,
        },
    )
