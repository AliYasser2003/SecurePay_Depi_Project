# SecurePay Secrets Management Plan

## Objective
Protect sensitive credentials and prevent them from being exposed in source code, GitHub, or application logs.

## Strategy

| Area | Approach |
|---|---|
| AWS authentication | GitHub OIDC instead of long-lived AWS keys |
| Application secrets | AWS Secrets Manager |
| Lambda access | IAM permission for specific secrets only |
| GitHub secrets | Store required deployment configuration securely |
| Secret exposure | Gitleaks scanning |
| Secret rotation | Rotate credentials when required |

## Rules
1. Never hardcode credentials in source code.
2. Never commit secrets to GitHub.
3. Never print secrets in application logs.
4. Give workloads access only to the secrets they need.
5. Rotate exposed or compromised credentials.

## Future Implementation
Use AWS Secrets Manager to store a test application secret and allow the required workload to retrieve it through IAM.

**Note:** Cognito manages user passwords; SecurePay does not store users' passwords itself.