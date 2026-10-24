k# SecurePay Cloud — Secure Coding Checklist

## 1. Input Validation

- [x] Validate payment amount range on the server.
- [x] Reject zero and negative payment amounts.
- [x] Test valid payment creation.
- [ ] Validate currency format beyond its current length constraint.
- [ ] Verify error responses do not expose internal details.

**Status:** Partially implemented. Five API tests passed locally. Additional validation and error-handling tests remain.

## 2. Authentication and Authorization

- [ ] Require authentication for protected endpoints.
- [ ] Verify permissions before allowing sensitive operations.
- [ ] Apply least privilege to application identities and roles.
- [ ] Test unauthorized and forbidden requests.

**Status:** Planned — authentication and authorization are not yet implemented.

## 3. Injection and Data Handling

- [ ] Use parameterized database queries.
- [ ] Avoid executing untrusted input as code or commands.
- [ ] Validate data exchanged between services.
- [ ] Avoid returning unnecessary sensitive information.

**Status:** Database controls will be reviewed when persistent storage and additional services are introduced.

## 4. Secrets and Configuration

- [x] Exclude local `.env` files through `.gitignore`.
- [x] Integrate Gitleaks into GitHub Actions.
- [x] Document secret storage, rotation, and incident response.
- [ ] Verify that `.env.example` contains placeholders only.
- [ ] Use a managed secrets service for cloud deployments.
- [ ] Configure and verify least-privilege workflow permissions.
- [ ] Rotate any credential that is exposed.

**Status:** Local secret-file exclusion, secret scanning, and documentation are implemented. Cloud secrets management and permission review remain pending.

## 5. Dependencies and Source Code

- [x] Run Bandit against application code in CI.
- [x] Run pip-audit against Python dependencies in CI.
- [x] Integrate automated tests into CI.
- [x] Document security scan results.
- [ ] Review and remediate future security findings.
- [ ] Establish a regular dependency update and review process.

**Status:** Bandit, pip-audit, and automated tests are integrated into GitHub Actions. Continue reviewing findings and maintaining dependencies.

## 6. Logging and Error Handling

- [ ] Verify that credentials and secrets are never logged.
- [ ] Verify that stack traces and internal details are not exposed to API clients.
- [ ] Record security-relevant events where appropriate.
- [ ] Protect logs against unauthorized access and modification.

**Status:** Pending verification and implementation as the application grows.

## 7. API and Deployment Security

- [x] Add the `X-Content-Type-Options: nosniff` HTTP response header.
- [x] Integrate OWASP ZAP Baseline scanning into GitHub Actions.
- [ ] Configure authentication and authorization before protected deployment.
- [ ] Implement and test rate limiting and request-size limits.
- [ ] Scan container images for known vulnerabilities.
- [ ] Inject secrets securely at runtime.
- [ ] Restrict network access and service permissions.
- [ ] Configure monitoring and an incident response process.

**Status:** The HTTP security header and ZAP Baseline CI scan are implemented. Container, cloud, and additional API controls remain planned.

## 8. Verification Record

| Check | Current status |
|---|---|
| Automated API tests | Implemented; 5 tests passed locally |
| Bandit SAST | Integrated into CI |
| pip-audit SCA | Integrated into CI |
| Gitleaks secret scanning | Integrated into CI |
| OWASP ZAP DAST | Integrated into CI; workflow run #6 passed |
| HTTP security header | Implemented and verified locally |
| Threat model | Documented |
| CI/CD security architecture | Documented |
| Secrets management plan | Documented |
| Authentication and authorization | Planned |
| Container security controls | Planned |

## 9. Review Rule

Mark a control as complete only after it has been implemented and verified. Documentation of a planned control does not mean that the control is deployed.

Update this checklist as the application architecture, dependencies, CI/CD pipeline, and deployment environment change.

