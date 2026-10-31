# SecurePay Week 2 — Identity, API and Serverless Security

## 1. Overview

Week 2 implements a simulated payment API using native AWS CloudFormation. The application demonstrates authenticated API access, request validation, serverless execution, and deployment artifact management.

The infrastructure is deployed using AWS CloudFormation resource types rather than AWS SAM.

## 2. Objectives

- Deploy AWS infrastructure using native CloudFormation.
- Authenticate API requests using Amazon Cognito.
- Expose a payment endpoint through Amazon API Gateway.
- Execute payment simulation logic using AWS Lambda and Python 3.12.
- Validate request bodies and reject invalid payment requests.
- Package Lambda application code into a ZIP artifact stored in Amazon S3.
- Test authentication and input validation using curl.
- Keep infrastructure deployment reproducible and version-controlled.

## 3. Architecture

The request flow is:

1. A client obtains an authentication token from Amazon Cognito.
2. The client sends a POST request to the API Gateway `/payments` endpoint.
3. The API Gateway Cognito authorizer validates the token.
4. API Gateway validates the request body against the configured request model.
5. Valid requests invoke the AWS Lambda function.
6. Lambda validates the payment data and returns a JSON response.
7. API Gateway returns the response to the client.

The payment operation is simulated. No actual financial transaction is performed.

## 4. AWS Services

| Service | Purpose |
|---|---|
| AWS CloudFormation | Provisions and manages the infrastructure |
| Amazon Cognito | User authentication and token issuance |
| Amazon API Gateway | Exposes and protects the payment API |
| AWS Lambda | Executes the Python payment handler |
| Amazon S3 | Stores the Lambda deployment ZIP |
| Amazon CloudWatch Logs | Provides Lambda execution logs |
| AWS IAM | Defines permissions for the Lambda execution role |

## 5. Technology Stack

- Python 3.12
- AWS CLI
- AWS CloudFormation
- Amazon Cognito
- Amazon API Gateway REST API
- AWS Lambda
- Amazon S3
- pytest
- curl
- Git and GitHub

## 6. Repository Structure

```text
SecurePay_Depi_Project/
├── cloudformation/
│   ├── template.yaml
│   ├── payment-function.zip
│   └── build/
│       └── handler.py
├── serverless/
│   ├── src/
│   │   └── handler.py
│   └── tests/
│       └── test_handler.py
├── docs/
│   └── week-2.md
└── README.md
```

The `serverless/` directory retains the application source and tests. The active deployment template is `cloudformation/template.yaml`; the project does not use AWS SAM for this deployment.

## 7. Deployment Procedure

### Validate the template

```bash
aws cloudformation validate-template \
  --template-body file://cloudformation/template.yaml \
  --region us-east-1
```

### Package the Lambda function

```bash
mkdir -p cloudformation/build

cp serverless/src/handler.py cloudformation/build/handler.py

cd cloudformation/build
zip -j ../payment-function.zip handler.py
cd ../..
```

The ZIP must contain `handler.py` at its root because the Lambda handler is configured as `handler.lambda_handler`.

### Upload the artifact

Set the deployment bucket:

```bash
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
BUCKET="securepay-artifacts-${ACCOUNT_ID}-us-east-1"
```

Upload the ZIP:

```bash
aws s3 cp cloudformation/payment-function.zip \
  "s3://${BUCKET}/week2/payment-function.zip" \
  --region us-east-1
```

### Deploy the infrastructure

```bash
aws cloudformation deploy \
  --template-file cloudformation/template.yaml \
  --stack-name securepay-week2 \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides DeploymentBucket="$BUCKET" \
  --region us-east-1
```

### Verify the stack

```bash
aws cloudformation describe-stacks \
  --stack-name securepay-week2 \
  --region us-east-1 \
  --query 'Stacks[0].StackStatus' \
  --output text
```

The last confirmed deployment status was `UPDATE_COMPLETE`.

## 8. Security Controls

### Authentication

The API uses an Amazon Cognito user pool authorizer. Requests without a valid authentication token are rejected.

### Request validation

The API request model validates the payment payload. The tested requirements include:

- A positive payment amount within the configured maximum.
- A three-letter uppercase currency code.
- Required request fields.

### Lambda execution permissions

The Lambda function runs using an IAM execution role defined in CloudFormation.

### Logging

Lambda execution logs are available through Amazon CloudWatch Logs.

## 9. Verification Results

The following results were observed during API testing:

| Scenario | Expected status | Observed status |
|---|---:|---:|
| Valid authenticated payment request | 201 | 201 |
| Missing authentication token | 401 or 403 | 401 |
| Invalid authentication token | 401 or 403 | 401 |
| Negative payment amount | 400 | 400 |
| Lowercase currency code | 400 | 400 |
| Missing currency field | 400 | 400 |

Successful request response:

```json
{
  "message": "Payment request accepted for simulation",
  "amount": "100",
  "currency": "USD",
  "simulated": true
}
```

These results verify the tested scenarios. They do not establish that every possible security scenario has been tested.

The Lambda configuration was also verified as active, with a successful last update, Python 3.12, and the handler `handler.lambda_handler`.

## 10. Automated Tests

Run the application unit tests with:

```bash
python -m pytest -v serverless/tests
```

Record the actual test count and result after the final test run.

## 11. Deployment Approach

This implementation uses native AWS CloudFormation.

The template defines resources such as:

- `AWS::Lambda::Function`
- `AWS::ApiGateway::RestApi`
- `AWS::ApiGateway::Authorizer`
- Other supporting API, Cognito, and IAM resources.

Lambda code is packaged separately and stored in S3. CloudFormation references the bucket and object when deploying the function.

AWS SAM is not used by the active Week 2 deployment.

## 12. Cleanup

After all testing and documentation are complete, delete the CloudFormation stack:

```bash
aws cloudformation delete-stack \
  --stack-name securepay-week2 \
  --region us-east-1
```

Wait for deletion:

```bash
aws cloudformation wait stack-delete-complete \
  --stack-name securepay-week2 \
  --region us-east-1
```

Confirm the stack has been removed:

```bash
aws cloudformation describe-stacks \
  --stack-name securepay-week2 \
  --region us-east-1
```

The final command should report that the stack does not exist.

After confirming stack deletion, remove the deployment ZIP from S3 and delete the artifact bucket if it is dedicated to this project and contains no other required files.

**Important:** Deleting the stack removes the deployed resources. Keep the CloudFormation template, application source, tests, and documentation in the repository.

## 13. Outcome

Week 2 demonstrates an authenticated serverless API deployed through native AWS CloudFormation. It covers infrastructure as code, identity management, API authorization, request validation, Lambda deployment packaging, and verification using HTTP requests.

The implementation provides a foundation for later work on secure CI/CD, automated security scanning, container security, and compliance controls.
