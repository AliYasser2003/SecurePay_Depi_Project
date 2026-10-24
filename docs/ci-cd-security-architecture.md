# SecurePay Cloud — CI/CD Security Architecture

## 1. Purpose

This document describes the secure Continuous Integration and Continuous Delivery (CI/CD) pipeline implemented for SecurePay Cloud. The pipeline automates application testing and security checks whenever code is pushed to the `main` branch or a pull request targets `main`.

## 2. Pipeline Architecture

```text
Developer
    |
    v
GitHub Repository
    |
    +---- Push to main / Pull Request
                 |
                 v
          GitHub Actions
                 |
                 v
          Checkout Source Code
                 |
                 v
          Set Up Python 3.12
                 |
                 v
          Install Dependencies
                 |
                 v
          Automated Tests (Pytest)
                 |
                 v
          SAST (Bandit)
                 |
                 v
          SCA (pip-audit)
                 |
                 v
          Secret Scanning (Gitleaks)
                 |
                 v
          Start FastAPI Application
                 |
                 v
          DAST (OWASP ZAP Baseline)
                 |
                 v
          Workflow Result and Logs
```

## 3. Implemented Security Controls

| Control | Tool | Purpose |
|---|---|---|
| Automated testing | Pytest | Verify API behavior and input validation |
| Static Application Security Testing (SAST) | Bandit | Detect potential Python security issues |
| Software Composition Analysis (SCA) | pip-audit | Identify known vulnerabilities in Python dependencies |
| Secret scanning | Gitleaks | Detect potential secrets in repository history |
| Dynamic Application Security Testing (DAST) | OWASP ZAP Baseline | Check the running API for common web security issues |
| HTTP security header | FastAPI middleware | Add `X-Content-Type-Options: nosniff` to responses |

## 4. Trigger Conditions

The workflow is configured to run when:
- Code is pushed to the `main` branch.
- A pull request targets the `main` branch.

The workflow configuration is located at `.github/workflows/ci.yml`.

## 5. Execution Environment

- CI platform: GitHub Actions
- Runner: `ubuntu-latest`
- Python version: 3.12
- Application framework: FastAPI
- DAST execution: OWASP ZAP Docker image
- API target during CI: `http://127.0.0.1:8000`

The API is started inside the GitHub Actions runner for the DAST step. The scan does not target the developer's local computer.

## 6. Failure Handling and Results

The workflow reports the result of each step in GitHub Actions logs. Steps configured to fail the workflow when a check fails help prevent unnoticed security regressions.

The ZAP Baseline scan uses the `-I` option so warnings alone do not cause a non-zero exit status. This does not suppress the warnings from the output. Scan results must still be reviewed.

## 7. Secrets and Permissions

- The Gitleaks action receives the GitHub-provided `GITHUB_TOKEN`.
- The repository must not contain real credentials, API keys, or production secrets.
- GitHub Actions permissions should follow the principle of least privilege.
- AWS credentials, OIDC configuration, secret rotation, and production secret storage are not yet implemented and will be addressed in the secrets management plan and later project phases.

## 8. Current Limitations

- The application is an educational prototype and does not process real payments.
- The pipeline does not replace manual security review or comprehensive penetration testing.
- The current DAST step uses ZAP Baseline, not a full active penetration test.
- AWS deployment, artifact signing, and production release controls remain future work.
- A successful workflow does not prove that the application is free of vulnerabilities.

## 9. Verification Evidence

The GitHub Actions workflow run associated with commit `db02a00` completed successfully after DAST integration. Subsequent successful workflow runs should also be checked when this document is submitted.

Evidence to retain:
- GitHub Actions run logs.
- Pytest output.
- Bandit and pip-audit results.
- Gitleaks scan results.
- OWASP ZAP output.
- Commits containing pipeline changes.

## 10. Review Checklist

- [x] Automated tests run in CI.
- [x] Bandit SAST is integrated.
- [x] pip-audit SCA is integrated.
- [x] Gitleaks secret scanning is integrated.
- [x] OWASP ZAP Baseline is integrated.
- [x] A basic HTTP security header is implemented.
- [ ] Least-privilege workflow permissions reviewed and documented.
- [ ] Secrets management plan completed.
- [ ] Artifact signing implemented and verified.

