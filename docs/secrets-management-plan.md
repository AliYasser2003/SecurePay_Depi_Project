# SecurePay Cloud — Secrets Management Plan

## 1. Purpose

This document defines how secrets and sensitive configuration should be handled during development, CI/CD, and future deployment of SecurePay Cloud.

The application is an educational payment-processing simulation. No real payment card data, production credentials, or real customer secrets should be used.

## 2. Secrets in Scope

Examples of secrets that may be introduced in later phases include:

- Database passwords and connection credentials.
- API keys and third-party service tokens.
- AWS access credentials, if required by an approved workflow.
- Authentication signing keys and application secrets.
- Deployment credentials and private certificates.

Public configuration, such as application names and non-sensitive feature settings, should be separated from secrets.

## 3. Local Development

- Store local secrets in environment variables or an untracked `.env` file.
- Keep `.env` and `.env.*` excluded through `.gitignore`, while allowing `.env.example`.
- Commit only placeholder values in `.env.example`; never include real credentials.
- Do not place passwords, tokens, or private keys directly in source code.
- Use simulated data for development and testing.

## 4. GitHub Actions

- Use GitHub Actions secrets or environment-scoped secrets only when a workflow requires them.
- Never print secrets to workflow logs.
- Avoid passing secrets as command-line arguments where they may be exposed.
- Grant the workflow only the repository permissions it needs.
- Review third-party actions before using them and pin actions to immutable commit SHAs when appropriate for the project's security requirements.
- The current Gitleaks step uses GitHub's provided `GITHUB_TOKEN`. No AWS deployment credentials are currently configured in the pipeline.

## 5. Future AWS Deployment

When AWS integration is introduced:

- Prefer GitHub Actions OIDC federation with AWS IAM roles over long-lived AWS access keys.
- Restrict the IAM role trust policy to the intended repository, branch, or deployment environment.
- Grant only the AWS permissions required for each deployment task.
- Store application secrets in AWS Secrets Manager or AWS Systems Manager Parameter Store, selecting the service according to the sensitivity and rotation requirements.
- Avoid embedding credentials in container images, Terraform files, source code, or logs.
- Review AWS resource permissions and access policies before deployment.

These controls are planned and are not yet implemented in the current local prototype.

## 6. Secret Rotation and Revocation

When a secret is suspected to be exposed:

1. Revoke or rotate the affected credential immediately.
2. Identify the affected services, workflows, and environments.
3. Review relevant logs for suspicious use.
4. Remove the exposed value from active configuration and source history where appropriate.
5. Validate the replacement credential and document the incident.
6. Review the cause of exposure and improve preventive controls.

Deleting a secret from the latest commit alone does not invalidate it and may not remove it from Git history.

## 7. Secret Scanning and Prevention

- Gitleaks is integrated into the CI workflow.
- The repository `.gitignore` excludes local `.env` files.
- Developers should review scan findings and investigate potential false positives.
- If a real secret is detected, treat it as exposed and rotate it rather than relying only on deleting the file.
- Periodically review repository history and workflow permissions.

## 8. Responsibilities

For this educational project, the project maintainer is responsible for:

- Keeping secrets out of source control.
- Reviewing secret-scanning results.
- Restricting CI permissions.
- Rotating exposed credentials.
- Reviewing AWS identity and secrets controls before cloud deployment.

## 9. Current Status

| Control | Status |
|---|---|
| `.env` exclusion in `.gitignore` | Implemented |
| Gitleaks in GitHub Actions | Implemented |
| Local `.env.example` convention | Documented |
| GitHub Actions least-privilege permissions review | Pending |
| AWS OIDC federation | Planned |
| AWS Secrets Manager or Parameter Store | Planned |
| Automated rotation | Planned, subject to service requirements |
| Production incident-response process | Not implemented; response steps documented |

## 10. Limitations

This document describes the current prototype and planned future controls. It does not claim that AWS identity federation, centralized secret storage, automated rotation, or production incident response has already been deployed.

No real payment credentials or real customer data should be introduced into this educational project.
