# SecurePay Cloud — Threat Model

## 1. Project Overview

SecurePay Cloud is an educational payment-processing application. It simulates payment requests and does not process real payments or store real payment-card data.

**Current implementation:** FastAPI application with server-side payment validation, automated tests, an HTTP security header, and a GitHub Actions CI pipeline that includes SAST, SCA, secret scanning, and DAST.

**Security objective:** Protect the integrity and availability of payment operations, prevent unauthorized access, and avoid exposing secrets or sensitive information.

## 2. Assets to Protect

| Asset | Security objective |
|---|---|
| Payment requests and amounts | Integrity and validation |
| Future payment and transaction records | Integrity and confidentiality |
| API endpoints | Authentication and authorization |
| Application configuration and secrets | Confidentiality |
| Source code and Git history | Integrity and secret protection |
| Python dependencies | Vulnerability management |
| CI/CD pipeline | Integrity and least privilege |
| Future audit records | Integrity and traceability |

## 3. Trust Boundaries

1. **External client → API:** Requests are untrusted and require server-side validation.
2. **Developer workstation → GitHub:** Source code must be reviewed and scanned before merging.
3. **GitHub Actions → build and test environment:** Workflow permissions and dependencies must be controlled.
4. **Application → database and other services:** Future service communication must be authenticated and restricted.
5. **AWS services → application:** Future cloud identities, network access, and secrets must follow least privilege.

## 4. Threats and Mitigations

| ID | Threat | Potential impact | Mitigation and status |
|---|---|---|---|
| T-01 | Invalid or manipulated payment amount | Incorrect simulated transaction | Server-side amount validation and automated tests implemented; additional validation tests remain |
| T-02 | Unauthorized access to payment endpoints | Unauthorized payment operations | Authentication and authorization planned; not implemented |
| T-03 | Injection through malicious input | Data exposure or unintended operations | Input validation implemented for current fields; database safeguards and broader security tests remain planned |
| T-04 | Credentials committed to Git | Unauthorized access to connected services | Gitleaks integrated into CI; managed secret storage and rotation procedures documented but not fully implemented |
| T-05 | Vulnerable third-party dependency | Exploitation of a known vulnerability | pip-audit integrated into CI |
| T-06 | Insecure application code | Application compromise | Bandit integrated into CI; code review and additional secure coding checks remain necessary |
| T-07 | Excessive CI/CD permissions | Unauthorized repository or cloud changes | Least-privilege permission review remains pending; AWS OIDC is planned |
| T-08 | Sensitive information in logs or responses | Information disclosure | Response minimization and logging controls require further verification |
| T-09 | Abuse or excessive API requests | Service disruption | Rate limiting and monitoring planned for the API security phase |
| T-10 | Compromised container image | Deployment of vulnerable or malicious software | Image scanning, controlled registries, and artifact signing planned for the container phase |
| T-11 | Missing HTTP content-sniffing protection | Browser may interpret content as a different media type | `X-Content-Type-Options: nosniff` header implemented and verified locally |

## 5. Existing Controls

- FastAPI request validation for payment amount range and currency length.
- Five automated API tests, including valid payment creation and rejection of zero and negative amounts.
- Bandit source-code scanning in GitHub Actions.
- pip-audit dependency vulnerability scanning in GitHub Actions.
- Gitleaks secret scanning in GitHub Actions.
- OWASP ZAP Baseline scanning integrated into GitHub Actions.
- `X-Content-Type-Options: nosniff` response header.
- GitHub Actions workflow triggered by pushes to `main` and pull requests targeting `main`.
- `.gitignore` rules excluding local `.env` files.

## 6. Planned Controls

- Additional tests for currency format, error handling, and security edge cases.
- Authentication and authorization for protected endpoints.
- API Gateway, Cognito, and WAF security controls.
- Container image scanning and runtime security.
- Secure secrets injection and least-privilege AWS IAM roles.
- GitHub Actions OIDC federation for AWS access.
- Monitoring, incident response, backup, and recovery controls.
- Artifact signing and verification.
- Rate limiting and request-size controls.

## 7. Assumptions and Limitations

- All payment activity is simulated.
- No real payment-card data or real financial transactions are in scope.
- Current security scans detect only the issue types covered by their rules and databases.
- The ZAP Baseline scan is a limited dynamic security scan and does not replace comprehensive penetration testing.
- Authentication, persistent storage, rate limiting, and cloud deployment controls are not yet implemented in the initial local application.
- A successful CI run does not prove that the application is free of vulnerabilities.
- This threat model is a working document and must be updated as the architecture changes.

## 8. Review Checklist

- [ ] Review threats when new endpoints or services are introduced.
- [ ] Reassess authentication and authorization before cloud deployment.
- [ ] Record security scan results and remediation decisions.
- [ ] Review CI/CD permissions before connecting AWS.
- [ ] Update the threat model when risks or controls change.
- [ ] Review this document before each major architecture change.

