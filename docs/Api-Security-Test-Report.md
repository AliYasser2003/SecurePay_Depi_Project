# SecurePay API Security Test Report

## Objective
Document security testing performed against the SecurePay API.

## Testing Tools
- Pytest — automated API and application tests.
- OWASP ZAP — automated dynamic application security scanning.

## Security Test Scope

| Test | Expected behavior |
|---|---|
| Missing authentication token | Reject request |
| Invalid authentication token | Reject request |
| Invalid payment amount | Reject request |
| Invalid currency format | Reject request |
| Missing required fields | Reject request |
| Malformed or malicious input | Reject invalid input |

## Results
The project already contains automated tests and an OWASP ZAP CI/CD scanning step.

## Conclusion
Automated testing and DAST scanning are integrated into the SecurePay security workflow. This report should be updated with the latest execution evidence.
## Latest Validation Evidence — November 2026

| Check | Result | Evidence |
|---|---|---|
| Cognito authentication and customer payment | PASS | Authenticated POST `/dev/payments` returned HTTP 201. |
| Lambda RBAC | PARTIAL | Customer group access succeeded; administrator and unauthorized-group rejection tests remain pending. |
| WAF association | PASS | Web ACL association and three managed rule groups were verified. |
| WAF SQL injection blocking | INCONCLUSIVE | A test returned HTTP 403, but the response did not establish that WAF caused the rejection. |
| Lambda IAM permissions | PASS | Only `AWSLambdaBasicExecutionRole` is attached; no inline policies were found. |
| CloudFormation deployment | PASS | Stack `securepay-week2` deployed successfully after adding the Cognito groups. |
| Git whitespace validation | PASS | `git diff --check` returned no errors. |

## Outstanding Validation
- Confirm WAF blocking behavior with evidence that identifies the blocking component.
- Test administrator permissions and rejection of users without an authorized group.
- Complete and review automated test execution evidence before claiming the full test suite passed.
