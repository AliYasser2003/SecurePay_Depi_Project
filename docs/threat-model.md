# SecurePay Cloud — Threat Model

## 1. Project Overview

SecurePay Cloud is an educational payment-processing application. It simulates payment requests and does not process real payments or store real payment-card data.

**Current implementation:** FastAPI application with payment validation, automated tests, and a GitHub Actions CI pipeline.

**Security objective:** Protect the integrity and availability of payment operations, prevent unauthorized access, and avoid exposing secrets or sensitive information.

## 2. Assets to Protect

| Asset | Security objective |
|---|---|
| Payment requests and amounts | Integrity and validation |
| Payment and transaction records | Integrity and confidentiality |
| API endpoints | Authentication and authorization |
| Application configuration and secrets | Confidentiality |
| Source code and Git history | Integrity and secret protection |
| Python dependencies | Vulnerability management |
| CI/CD pipeline | Integrity and least privilege |
| Audit records | Integrity and traceability |

## 3. Trust Boundaries

1. **External client → API:** Requests are untrusted and require validation.
2. **Developer workstation → GitHub:** Source code must be reviewed and scanned before merging.
3. **GitHub Actions → build and test environment:** Workflow permissions and dependencies must be controlled.
4. **Application → database and other services:** Future service communication must be authenticated and restricted.
5. **AWS services → application:** Future cloud identities, network access, and secrets must follow least privilege.

## 4. Threats and Mitigations

| ID | Threat | Potential impact | Planned mitigation |
|---|---|---|---|
| T-01 | Invalid or manipulated payment amount | Incorrect simulated transaction | Server-side validation and automated negative-input tests |
| T-02 | Unauthorized access to payment endpoints | Unauthorized payment operations | Add authentication and authorization before production-like deployment |
| T-03 | Injection through malicious input | Data exposure or unintended operations | Input validation, safe database queries, and security testing |
| T-04 | Credentials committed to Git | Unauthorized access to connected services | Gitleaks scanning, secret management, and credential rotation if exposed |
| T-05 | Vulnerable third-party dependency | Exploitation of a known vulnerability | pip-audit, dependency updates, and CI security gates |
| T-06 | Insecure application code | Application compromise | Bandit SAST, code review, and secure coding practices |
| T-07 | Excessive CI/CD permissions | Unauthorized repository or cloud changes | Least-privilege workflow permissions and short-lived AWS credentials |
| T-08 | Sensitive information in logs or responses | Information disclosure | Avoid logging secrets and minimize sensitive response data |
| T-09 | Abuse or excessive API requests | Service disruption | Add rate limiting and monitoring in the API security phase |
| T-10 | Compromised container image | Deployment of vulnerable or malicious software | Image scanning, controlled registries, and artifact signing |

## 5. Existing Controls

- FastAPI request validation for payment amounts and currency length.
- Five automated API tests.
- Bandit source-code scanning.
- pip-audit dependency vulnerability scanning.
- Gitleaks secret scanning.
- GitHub Actions workflow triggered by pushes and pull requests.

## 6. Planned Controls

- Threat-driven security tests and a secure coding checklist.
- Authentication and authorization for protected endpoints.
- API Gateway, Cognito, and WAF security controls.
- Container image scanning and runtime security.
- Secure secrets injection and least-privilege AWS IAM roles.
- Monitoring, incident response, backup, and recovery controls.

## 7. Assumptions and Limitations

- All payment activity is simulated.
- No real payment-card data or real financial transactions are in scope.
- Current security scans detect only the issue types covered by their rules and databases.
- Authentication, persistent storage, rate limiting, and cloud deployment controls are not yet implemented in the initial local application.
- This threat model is a working document and must be updated as the architecture changes.

## 8. Review Checklist

- [ ] Review threats when new endpoints or services are introduced.
- [ ] Reassess authentication and authorization before cloud deployment.
- [ ] Record security scan results and remediation decisions.
- [ ] Review CI/CD permissions before connecting AWS.
- [ ] Update the threat model when risks or controls change.
