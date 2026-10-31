## Week 2 — Identity, API and Serverless Security

### Overview

Week 2 implements a simulated payment API using native AWS CloudFormation, Amazon Cognito, Amazon API Gateway, AWS Lambda, and Amazon S3.

The API requires authentication and validates payment request bodies before processing the simulation.

### Architecture

```text
Client
  |
  | Cognito authentication
  v
Amazon Cognito
  |
  | Authentication token
  v
Amazon API Gateway REST API
  |
  | Cognito authorizer
  | Request model validation
  v
AWS Lambda — Python 3.12
  |
  v
Simulated payment response
```

The Lambda deployment package is stored in Amazon S3 and referenced by the CloudFormation template.

### Technologies

- Native AWS CloudFormation
- Amazon Cognito
- Amazon API Gateway REST API
- AWS Lambda
- Amazon S3
- AWS IAM
- Amazon CloudWatch Logs
- Python 3.12
- pytest
- AWS CLI

### Deployment

Validate the template:

```bash
aws cloudformation validate-template \
  --template-body file://cloudformation/template.yaml \
  --region us-east-1
```

Deploy the stack:

```bash
aws cloudformation deploy \
  --template-file cloudformation/template.yaml \
  --stack-name securepay-week2 \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides DeploymentBucket="$BUCKET" \
  --region us-east-1
```

### Testing

Run unit tests:

```bash
python -m pytest -v serverless/tests
```

The API was tested with an authenticated payment request and requests containing missing or invalid authentication, a negative amount, a lowercase currency code, and a missing currency field.

Observed results were HTTP 201 for the valid request and HTTP 401 or 400 for the tested invalid requests, as appropriate.

### Documentation

See [`docs/week-2.md`](docs/week-2.md) for the detailed architecture, deployment steps, security controls, verification results, and cleanup procedure.

### Deployment Method

The active Week 2 implementation uses native AWS CloudFormation. AWS SAM is not used to deploy this stack. The application source and tests remain under `serverless/`, while the infrastructure template is maintained under `cloudformation/`.

### Important Note

The payment endpoint simulates payment processing only. It does not initiate or settle real payment
