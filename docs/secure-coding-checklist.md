# SecurePay Cloud — Secure Coding Checklist

## 1. Input Validation

- [ ] Validate all client input on the server.
- [ ] Reject missing, malformed, or out-of-range values.
- [ ] Enforce valid payment amounts and currency formats.
- [ ] Return appropriate error responses without exposing internal details.

## 2. Authentication and Authorization

- [ ] Require authentication for protected endpoints.
- [ ] Verify permissions before allowing sensitive operations.
- [ ] Apply least privilege to application identities and roles.
- [ ] Test unauthorized and forbidden requests.

*Status: Planned — authentication and authorization are not yet implemented.*

## 3. Injection and Data Handling

- [ ] Use parameterized database queries.
- [ ] Avoid executing untrusted input as code or commands.
- [ ] Validate data exchanged between services.
- [ ] Avoid returning unnecessary sensitive information.

*Status: Database controls will be reviewed when persistent storage is introduced.*

## 4. Secrets and Configuration

- [ ] Never commit passwords, API keys, or access tokens.
- [ ] Run Gitleaks against the repository and its Git history.
- [ ] Store local secrets outside source control.
- [ ] Use a managed secrets service for cloud deployments.
- [ ] Rotate any credential that is exposed.

## 5. Dependencies and Source Code

- [ ] Run Bandit against application code.
- [ ] Run pip-audit against Python dependencies.
- [ ] Review security findings and document remediation.
- [ ] Keep dependencies updated using compatible, tested versions.
- [ ] Require tests and security checks to pass in CI.

## 6. Logging and Error Handling

- [ ] Do not log credentials or other secrets.
- [ ] Avoid exposing stack traces to API clients.
- [ ] Record security-relevant events where appropriate.
- [ ] Protect logs against unauthorized access and modification.

## 7. API and Deployment Security

- [ ] Configure authentication and authorization before protected deployment.
- [ ] Apply rate limiting and request-size limits.
- [ ] Scan container images for known vulnerabilities.
- [ ] Inject secrets securely at runtime.
- [ ] Restrict network access and service permissions.
- [ ] Enable monitoring and define an incident response process.

*Status: Planned — deployment controls will be verified in later project phases.*

## 8. Verification Record

| Check                                         | Current status                      |
---------------------------------------------------------------------------------------
| Automated API tests                           | Implemented; 5 tests passed locally |
| Bandit SAST                                   | Integrated into CI                  |
| pip-audit SCA                                 | Integrated into CI                  |
| Gitleaks secret scanning                      | Integrated into CI                  |
| OWASP ZAP DAST                                | Planned                             |
| Authentication and authorization              | Planne                              |
| Container security controls                   | Planned                             |

**Review rule:** Mark a control as complete only after it has been implemented and verified. Update this checklist as the application architecture changes.
