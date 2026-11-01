# SecurePay Cloud — Phase 2: Identity, API, and Serverless Security

## Overview
Phase 2 deploys a simulated payment API to AWS using native AWS CloudFormation. Amazon Cognito provides user identity tokens, API Gateway protects the endpoint with a Cognito authorizer, and AWS Lambda runs the Python 3.12 payment handler. No real financial transaction is performed.

## Request flow
1. A client authenticates with Amazon Cognito and obtains a token.
2. The client sends `POST /payments` with the token.
3. API Gateway's Cognito authorizer validates the token.
4. API Gateway validates the request structure against the configured model.
5. Lambda performs application-level payment validation and returns a simulated result.
6. API Gateway returns the response.

See [Phase 2 architecture](architecture/phase-2-serverless-api.svg).

## AWS services

| Service | Role |
|---|---|
| AWS CloudFormation | Defines and deploys resources from `cloudformation/template.yaml` |
| Amazon Cognito | Provides application user identity and tokens |
| Amazon API Gateway | Exposes the API and applies authorization/request validation |
| AWS Lambda | Executes `handler.lambda_handler` using Python 3.12 |
| AWS IAM | Defines permissions for the Lambda execution role |
| Amazon S3 | Stores the Lambda deployment ZIP |
| Amazon CloudWatch Logs | Stores Lambda execution logs |

The deployment used stack name `securepay-week2` in `us-east-1`. These are historical details; the stack was later deleted to avoid ongoing costs. Confirm current AWS resource status before redeploying.

## Verification
Recorded tests showed a valid authenticated request returned HTTP 201;
missing or invalid tokens returned HTTP 401;
negative amount, lowercase currency, or missing currency returned HTTP 400.
The serverless test suite recorded 12 passing tests.
These results have not been rerun as part of this document update.

## Deployment outline
1. Validate `cloudformation/template.yaml`.
2. Package the Lambda handler into a ZIP with `handler.py` at the archive root.
3. Upload the ZIP to the project's S3 artifact bucket.
4. Deploy using AWS CLI and CloudFormation.
5. Test authentication and request validation.
6. Delete the stack and clean up dedicated artifact resources when finished.

This phase uses native CloudFormation.

## Scope and limitations
The endpoint simulates payment acceptance; it is not a production payment system. Selected tests do not establish complete security, compliance, or readiness for real cardholder data.
