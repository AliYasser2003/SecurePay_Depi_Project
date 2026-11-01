# SecurePay Threat Model

## Objective
Identify the main security threats affecting SecurePay and document their protections.

| Component | Threat | Mitigation |
|---|---|---|
| GitHub repository | Exposed credentials | Gitleaks |
| GitHub Actions | Unauthorized AWS access | GitHub OIDC and IAM trust policy |
| API Gateway | Unauthorized requests | Cognito authentication |
| Payment API | Malicious or invalid input | Request validation and security tests |
| Lambda | Excessive permissions | IAM least privilege |
| Deployment S3 bucket | Unauthorized artifact access | Restricted IAM and bucket access |

## Main Risks
- Stolen credentials.
- Unauthorized API access.
- Malicious payment input.
- Compromised deployment pipeline.
- Excessive AWS permissions.

## Conclusion
SecurePay uses automated security scanning, authentication, input validation, artifact signing, and restricted AWS permissions to reduce these risks.

This threat model describes the current educational project and does not guarantee complete protection.