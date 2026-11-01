# SecurePay Cloud — Phase 2: Identity, API, and Serverless Security

## Overview
Phase 2 deploys a simulated payment API using AWS CloudFormation. Amazon Cognito provides identity tokens, API Gateway authorizes requests, and AWS Lambda executes the Python 3.12 payment handler.

No real financial transactions are processed.

## Request Flow
1. The client authenticates through Cognito.
2. The client sends `POST /payments` with an ID token.
3. API Gateway validates the token.
4. API Gateway applies request validation.
5. Lambda enforces application-level validation and RBAC.
6. The API returns a simulated payment response.

Architecture: `architecture/phase-2-serverless-api.svg`

## AWS Services

| Service | Purpose |
|---|---|
| CloudFormation | Infrastructure deployment |
| Cognito | User identity, OAuth, and groups |
| API Gateway | API endpoint, authorization, and validation |
| Lambda | Payment request handler |
| IAM | Lambda execution permissions |
| S3 | Deployment artifact storage |
| CloudWatch Logs | Lambda execution logs |
| AWS WAF | Managed web-request protections |

## Deployment Status
The `securepay-week2` CloudFormation stack exists in `us-east-1`. Its resources include the payment Lambda, API Gateway, Cognito user pool, groups, authorizer, and API stage.

The API endpoint is:

`https://ieibzuamy3.execute-api.us-east-1.amazonaws.com/dev/payments`

The `securepay-week2-waf` Web ACL is associated with the API stage.

## Verification
- Authorized payment request: HTTP 201.
- Application validation errors: HTTP 400.
- Unauthorized access: HTTP 403, as reported by the project owner.
- Local unit tests: 15 passed.
- GitHub Actions: Reported passing by the project owner.

WAF association is confirmed; complete rule-behavior verification remains separate.

## Deployment Outline
1. Validate `cloudformation/template.yaml`.
2. Package `handler.py` at the ZIP archive root.
3. Upload the deployment ZIP to S3.
4. Deploy with AWS CLI and CloudFormation.
5. Test authentication, authorization, and request validation.
6. Clean up resources deliberately when no longer needed.

## Scope and Limitations
The API simulates payment acceptance and is not a production payment system. These tests do not establish full security, regulatory compliance, or readiness for cardholder data.
