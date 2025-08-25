# Security Policy

## Supported Versions

Currently supported versions of the TCGplayer Python Client:

| Version | Supported          | Security Updates |
| ------- | ------------------ | ---------------- |
| 2.0.3   | :white_check_mark: | :white_check_mark: |
| 2.0.2   | :white_check_mark: | :white_check_mark: |
| 2.0.x   | :white_check_mark: | :white_check_mark: |
| 1.0.x   | :x:                | :x:              |
| < 1.0   | :x:                | :x:              |

## Reporting a Vulnerability

If you discover a security vulnerability in the TCGplayer Python Client, please
follow responsible disclosure practices:

### 🚨 **DO NOT** create a public GitHub issue for security vulnerabilities

### ✅ **DO** report via these secure channels

1. **Email**: <josh@gobby.ai>
2. **Subject**: [SECURITY] TCGplayer Python Client Vulnerability
3. **Include**:
   - Detailed description of the vulnerability
   - Steps to reproduce
   - Potential impact assessment
   - Suggested fix (if any)

### ⏱️ **Response Timeline**

- **Initial Response**: Within 48 hours
- **Vulnerability Assessment**: Within 7 days
- **Fix Development**: Depends on severity
- **Public Disclosure**: After fix is released

## Security Measures

This project implements multiple layers of security:

### 🔒 **Code Security**

- ✅ Automated security scanning with Bandit
- ✅ Dependency vulnerability checks with pip-audit
- ✅ Static analysis with Semgrep
- ✅ CodeQL analysis for vulnerability detection
- ✅ Comprehensive dependency testing
- ✅ Build system validation

### 🛡️ **CI/CD Security**

- ✅ Pre-commit hooks for early detection
- ✅ Automated security workflows
- ✅ Dependency review for PRs
- ✅ Weekly security scans

### 📁 **Repository Security**

- ✅ Branch protection rules
- ✅ Required code reviews
- ✅ CODEOWNERS for sensitive files
- ✅ Comprehensive .gitignore

## Environment Variables & Secrets

### ⚠️ **NEVER commit these to the repository:**

- `.env` files
- `*.key` files
- `*.pem` files
- API credentials
- Database connection strings
- Any secrets or sensitive data

### ✅ **DO use for local development:**

- `.env.example` as a template
- Environment variables for configuration
- Secure credential storage
- Virtual environments

## Development Security Guidelines

### 1. **API Credentials**

```bash

# Use environment variables

export TCGPLAYER_CLIENT_ID="your_client_id"
export TCGPLAYER_CLIENT_SECRET="your_client_secret"

# Never hardcode in source


# ❌ BAD

client = TCGPlayerClient(client_id="abc123", client_secret="xyz789")

# ✅ GOOD

client = TCGPlayerClient()  # Uses environment variables

```

### 2. **Dependency Management**

- Keep dependencies updated
- Review security advisories
- Use virtual environments
- Pin versions in production

### 3. **Code Quality**

- Run pre-commit hooks
- Follow secure coding practices
- Handle errors gracefully
- Validate all inputs

### 4. **Testing Security**

- Test with invalid inputs
- Test authentication failures
- Test rate limiting
- Mock external API calls

## Dependencies Security

### 🔍 **Regular Audits**

```bash

# Check for vulnerabilities

pip-audit
make security

# Update dependencies

pip install --upgrade package_name

# Run dependency tests

make test-deps
```

### 📦 **Trusted Sources**

- Only use packages from PyPI
- Verify package maintainers
- Review package source code for critical dependencies
- Monitor for typosquatting

## Incident Response

### 🚨 **If you suspect a security breach:**

1. **Immediate Actions**:
   - Rotate all API keys
   - Review access logs
   - Document the incident

2. **Contact**:
   - Email: <josh@gobby.ai>
   - Include: Timeline, impact, evidence

3. **Follow-up**:
   - Implement fixes
   - Update security measures
   - Post-incident review

## Security Resources

- **TCGplayer API Security**: <https://docs.tcgplayer.com/docs/authentication>
- **Python Security Guide**: <https://python-security.readthedocs.io/>
- **OWASP Top 10**: <https://owasp.org/www-project-top-ten/>
- **GitHub Security Features**: <https://docs.github.com/en/code-security>

## License

This security policy is part of the TCGplayer Python Client project and is
subject to the same license terms.

---

**Last Updated**: August 2025  
**Version**: 2.0.2  
**Maintainer**: Josh Wilhelmi (<josh@gobby.ai>)
