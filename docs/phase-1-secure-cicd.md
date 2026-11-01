# SecurePay Cloud — Phase 1: Secure CI/CD

## Overview
Phase 1 secures the software development and delivery workflow for the educational SecurePay API. It combines automated testing, source/dependency checks, web security scanning, secure workflow-to-AWS authentication, and artifact signing. SecurePay simulates payment requests; it does not process real payments.

## CI/CD flow
1. A push to `main` or a pull request triggers GitHub Actions.
2. The workflow checks out the repository, sets up Python 3.12, installs dependencies, and runs Pytest.
3. Bandit, `pip-audit`, and Gitleaks perform security checks.
4. The FastAPI application is started so OWASP ZAP Baseline can scan it over HTTP.
5. The workflow packages selected source files into `securepay-source.tar.gz`; Cosign signs and verifies the archive.
6. GitHub Actions OIDC and AWS IAM provide a federated identity path for obtaining temporary AWS credentials.

See [Phase 1 architecture](architecture/phase-1-ci-cd.svg).

## Security controls

| Control | Tool | Purpose |
|---|---|---|
| Automated testing | Pytest | Check expected application behavior |
| SAST | Bandit | Flag potentially risky Python patterns |
| SCA | `pip-audit` | Check dependencies for known vulnerabilities |
| Secret scanning | Gitleaks | Detect patterns that may indicate exposed secrets |
| DAST | OWASP ZAP Baseline | Passively scan the running API |
| Workflow identity | GitHub Actions OIDC + AWS IAM | Obtain temporary AWS credentials under configured trust conditions |
| Artifact signing | Cosign | Sign and verify the source archive |

## Recorded results
Project notes record five API tests passed locally; Bandit reported no medium/high-severity findings;
`pip-audit` reported no known dependency vulnerabilities;
Gitleaks found no leaks; and ZAP improved from 60 passing checks plus one missing-header warning to 61 passing checks with no warnings after adding `X-Content-Type-Options: nosniff`.

These are historical results, not a guarantee that the current code is vulnerability-free. Retain successful GitHub Actions runs as evidence for OIDC and Cosign.

## Scope and limitations
ZAP Baseline is not a full penetration test. Artifact signature verification depends on checking the expected signer identity and trust conditions. Application authentication, rate limiting, persistent transaction storage, and production operations are outside this phase's demonstrated scope.
