# SecurePay Cloud — Security Scan Results

## 1. Overview

SecurePay Cloud uses an automated CI pipeline to run application tests and security checks. The pipeline is configured in `.github/workflows/ci.yml` and runs on pushes to `main` and pull requests targeting `main`.

## 2. Security Tools and Results

| Check | Tool | Purpose | Result |
|---|---|---|---|
| Automated tests | Pytest | Verify application behavior and input validation | 5 tests passed |
| SAST | Bandit | Identify potential Python security issues | No medium/high severity issues reported |
| SCA | pip-audit | Check Python dependencies for known vulnerabilities | No known vulnerabilities found |
| Secret scanning | Gitleaks | Detect exposed secrets in repository history | No leaks found in local scan |
| DAST | OWASP ZAP Baseline | Check the running API for common web security issues | Initial scan: 60 PASS, 1 WARN; follow-up scan: 61 PASS |

## 3. Remediation

The initial ZAP scan reported a missing `X-Content-Type-Options` HTTP response header.

The application was updated to return:

`X-Content-Type-Options: nosniff`

A follow-up ZAP scan reported 61 passing checks and no warnings.

## 4. CI/CD Integration

The GitHub Actions workflow includes automated tests, Bandit, pip-audit, Gitleaks, and OWASP ZAP Baseline scanning.

Latest recorded workflow run: #6  
Commit: `db02a00`  
Status: Completed successfully.

## 5. Limitations

- A passing scan does not prove the application is free of vulnerabilities.
- ZAP Baseline is a limited scan and does not replace comprehensive penetration testing.
- The API is currently a prototype; authentication, persistent transaction storage, and production deployment security remain future work.
- Results should be refreshed whenever the application, dependencies, or pipeline changes.

## 6. Evidence to Retain

- GitHub Actions run logs for each security tool.
- Local OWASP ZAP output before and after remediation.
- Pytest output.
- Relevant repository commits.
