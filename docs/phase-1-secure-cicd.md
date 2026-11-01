# SecurePay Cloud — Phase 1: Secure CI/CD

## Overview
Phase 1 secures the development and delivery workflow for the educational SecurePay API. The application simulates payment requests and does not process real payments.

## CI/CD Flow
1. GitHub Actions triggers on pushes to `main` and pull requests.
2. Python 3.12 dependencies are installed and Pytest runs.
3. Bandit, `pip-audit`, and Gitleaks perform security checks.
4. OWASP ZAP Baseline scans the running API.
5. The workflow packages source files into `securepay-source.tar.gz`; Cosign signs and verifies the archive.
6. GitHub Actions OIDC federates with AWS IAM to obtain temporary credentials.

Architecture: `architecture/phase-1-ci-cd.svg`

## Security Controls

| Control | Tool |
|---|---|
| Automated testing | Pytest |
| SAST | Bandit |
| Dependency scanning | `pip-audit` |
| Secret scanning | Gitleaks |
| DAST | OWASP ZAP Baseline |
| Federated AWS access | GitHub Actions OIDC + IAM |
| Artifact signing | Cosign |

## Recorded Results
Historical results recorded successful tests and security scans. ZAP improved from 60 passing checks and one missing-header warning to 61 passing checks with no warnings after adding `X-Content-Type-Options: nosniff`.

These results do not guarantee that the current code is vulnerability-free. Use successful GitHub Actions runs to verify OIDC and Cosign.

## Scope and Limitations
ZAP Baseline is not a full penetration test. Signature verification must validate the expected signer identity. Production authentication, rate limiting, persistent transaction storage, and production operations are outside this phase's demonstrated scope.
