# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | ✅        |

## Reporting a Vulnerability

If you discover a security vulnerability in NeuroQuest, please email the maintainers at:
- **security@neuroquest.dev** (if available)
- Or create a private security advisory on GitHub

**Please do not open public issues for security vulnerabilities.**

### What to Include

When reporting a security issue, please include:
1. Description of the vulnerability
2. Steps to reproduce
3. Potential impact
4. Suggested fix (if available)
5. Your name and contact information (optional)

## Security Best Practices

### For Developers

1. **Never commit API keys or secrets**
   - Use `.env.example` as a template
   - Add `.env` to `.gitignore`
   - Use GitHub Secrets for CI/CD

2. **Keep dependencies updated**
   ```bash
   # Backend
   pip-audit
   pip list --outdated
   
   # Frontend
   npm audit
   npm outdated
   ```

3. **Use strong credentials**
   - JWT_SECRET_KEY: minimum 32 characters
   - ENCRYPTION_KEY: cryptographically random
   - Database passwords: strong and unique

4. **Enable security headers**
   - Content-Security-Policy
   - X-Content-Type-Options
   - X-Frame-Options
   - Strict-Transport-Security

### For Users

1. **Change default credentials**
   - Never use default database password
   - Generate strong JWT and encryption keys

2. **Keep software updated**
   - Update Python packages regularly
   - Update Node.js packages regularly
   - Apply system security patches

3. **Use HTTPS in production**
   - Obtain SSL certificate (Let's Encrypt)
   - Configure secure CORS origins
   - Use secure cookie flags

4. **Protect API keys**
   - Store in secure vault (AWS Secrets Manager, etc.)
   - Rotate periodically
   - Use key versioning
   - Monitor for unauthorized access

## Vulnerability Disclosure Timeline

1. **Initial Report**: Security team acknowledges within 48 hours
2. **Assessment**: Team assesses severity within 5 days
3. **Patch Development**: Critical patches prioritized
4. **Release**: Coordinated disclosure after fix is released
5. **Public Notification**: Security advisory published

## Security Headers

Ensure these are configured in production:

```python
@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response
```

## Dependencies Security

### Regular Audits

```bash
# Backend
pip install safety
safety check

# Frontend
npm audit
npm audit fix
```

### Pinned Versions

Keep dependencies pinned to known-good versions in production:

```
requirements.txt: fastapi==0.104.1
package.json: "react": "18.2.0"
```

## Encryption

- Database passwords: stored securely, never in code
- User data: encrypted at rest and in transit
- API keys: not logged or exposed in error messages
- JWT tokens: signed with strong secret, short expiration

## Rate Limiting

Implement rate limiting to prevent abuse:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/search")
@limiter.limit("10/minute")
def search(query: str):
    ...
```

## Logging & Monitoring

- Never log sensitive data (API keys, passwords, tokens)
- Monitor for suspicious access patterns
- Set up alerts for security events
- Archive logs securely
- Rotate logs regularly

## Compliance

This project may need to comply with:
- GDPR (if handling EU user data)
- CCPA (if handling California user data)
- HIPAA (if handling health data)
- SOC 2 (if providing to enterprises)

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)

---

Last Updated: April 2026
