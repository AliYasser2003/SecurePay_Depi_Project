# SecurePay Cloud — Week 1 Security Summary

## 1. Project Overview

SecurePay Cloud is an educational payment-processing application built with FastAPI. It simulates payment requests and does not process real financial transactions or store real payment-card data.

Week 1 establishes a secure development lifecycle through automated testing, security scanning, controlled AWS authentication, and build artifact signing.

## 2. CI/CD Architecture

The pipeline is defined in `.github/workflows/ci.yml` and uses GitHub Actions. It runs on pushes to `main` and pull requests targeting `main`.

The workflow checks out the repository, sets up Python 3.12, installs dependencies, and runs automated tests and security tools. The application is started in the CI environment for OWASP ZAP Baseline scanning.

Additional jobs authenticate to AWS through OpenID Connect (OIDC) and sign and verify build artifacts using Cosign.

## 3. Security Controls

| Control | Implementation | Purpose |
|---|---|---|
| Automated testing | Pytest | Verify API behavior and input validation |
| SAST | Bandit | Identify potential Python security issues |
| SCA | pip-audit | Detect known vulnerabilities in dependencies |
| Secret scanning | Gitleaks | Detect potentially exposed credentials |
| DAST | OWASP ZAP Baseline | Scan the running API for common web security issues |
| HTTP security | `X-Content-Type-Options: nosniff` | Reduce MIME-type sniffing risks |
| Cloud identity | GitHub Actions OIDC with AWS IAM | Authenticate without long-lived AWS access keys |
| Artifact integrity | Cosign signing and verification | Verify signed build artifacts |

## 4. Threat Model

The principal assets are payment request integrity, application configuration, credentials, source code, dependencies, and the CI/CD pipeline.

External requests may contain invalid or manipulated data. Compromised dependencies or leaked credentials could affect application security. Excessive workflow permissions or compromised build artifacts could undermine the software delivery process.

Current mitigations include server-side payment validation, automated tests, security scanning, local environment-file exclusions, restricted OIDC trust conditions, and artifact signing and verification.

Authentication and authorization for protected API operations, rate limiting, persistent transaction storage, container security, and production monitoring remain areas for future implementation.

## 5. Secrets Management

Local development must use simulated data and must not commit real credentials. Local `.env` files are excluded through `.gitignore`, and Gitleaks scans the repository through CI.

GitHub Actions uses OIDC to obtain temporary AWS role credentials rather than relying on long-lived AWS access keys. The IAM trust policy restricts role assumption to the intended GitHub repository and `main` branch.

Application secrets for a future deployment should be stored in an appropriate managed service, such as AWS Secrets Manager or Systems Manager Parameter Store. Exposed credentials must be revoked or rotated, and relevant logs and configuration must be reviewed.

Centralized application-secret storage and automated rotation have not yet been implemented.

## 6. Security Scan Results

The recorded results from the initial implementation are:

- **Pytest:** five API tests passed locally.
- **Bandit:** no medium- or high-severity issues reported in the recorded scan.
- **pip-audit:** no known dependency vulnerabilities reported in the recorded scan.
- **Gitleaks:** no leaks found in the recorded local scan.
- **OWASP ZAP Baseline:** the initial scan reported 60 passing checks and one warning about a missing HTTP security header. After the header was added, the follow-up scan reported 61 passing checks and no warnings.

These results describe the recorded scans, not a guarantee that the application is vulnerability-free. The latest successful GitHub Actions run should be retained as evidence for the completed pipeline, including the AWS OIDC and Cosign jobs.

## 7. Scope and Limitations

The project currently demonstrates secure CI/CD practices for an educational API. ZAP Baseline is not a comprehensive penetration test, and automated scans cannot identify every possible vulnerability.

The application does not yet provide a complete production payment system. Authentication and authorization, persistent transaction storage, rate limiting, and production operational controls require further work as the project develops.

