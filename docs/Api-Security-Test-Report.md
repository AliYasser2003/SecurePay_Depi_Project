# SecurePay API Security Test Records

## Objective
Record API security test cases, expected behavior, actual results, and supporting evidence.

## Test Records

| Test Case | Expected Result | Status | Evidence |
|---|---|---|---|
| Authenticated customer payment | HTTP 201 | PASS | Successful `POST /dev/payments` |
| Missing authentication token | HTTP 401 | PENDING | Capture response |
| Invalid authentication token | HTTP 401 | PENDING | Capture response |
| Invalid payment amount | HTTP 400 | PENDING | Capture response |
| Invalid currency format | HTTP 400 | PENDING | Capture response |
| Missing required fields | HTTP 400 | PENDING | Capture response |
| Malformed or malicious input | Reject invalid input | PENDING | Capture response and logs |
| Administrator access | Follow configured RBAC policy | PENDING | Capture response |
| User without an authorized group | HTTP 403 | PENDING | Capture response |
| WAF SQL injection protection | Block malicious request | INCONCLUSIVE | HTTP 403 observed; blocking component not confirmed |

## Test Execution

- **Automated tests:** Record the latest Pytest and CI/CD results after execution.
- **Dynamic scanning:** Attach the OWASP ZAP report from the relevant CI/CD run.
- **Manual tests:** Record the request, HTTP response, timestamp, and relevant logs.
- **Failed or inconclusive tests:** Investigate and retest before marking them PASS.

## Conclusion

The authenticated customer payment flow has been verified. Other test cases remain pending or inconclusive until supported by execution evidence.

**Note:** Expected HTTP status codes must be confirmed against the actual API behavior. A 403 response alone does not prove that AWS WAF blocked a request.
