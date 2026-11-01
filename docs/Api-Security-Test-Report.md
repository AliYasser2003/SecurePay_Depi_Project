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