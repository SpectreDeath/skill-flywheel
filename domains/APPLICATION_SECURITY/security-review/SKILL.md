---
name: security-review
description: "Use when: adding authentication, handling user input, working with secrets, creating API endpoints, implementing payment or sensitive features, or performing security audits. Triggers: 'security', 'auth', 'authentication', 'authorization', 'secure', 'API security', 'input validation', 'secrets', 'payment', 'sensitive data', 'security audit'. NOT for: public read-only endpoints, or when security has already been reviewed and approved."
---

# Security Review

Comprehensive security checklist and patterns for building secure applications.

## When to Use This Skill

Use this skill when:
- Adding authentication to an application
- Handling user input in API endpoints
- Working with secrets, API keys, passwords
- Creating new API endpoints
- Implementing payment or sensitive features
- Performing security code review
- Building any feature handling user data

Do NOT use when:
- Public read-only endpoints with no user data
- Already reviewed and approved code
- Simple static content

## Authentication Checklist

### Password Handling
```python
# NEVER store passwords in plain text
# ALWAYS use proper hashing (bcrypt, argon2, scrypt)

import hashlib  # NEVER use for passwords
from passlib.hash import bcrypt

# Correct approach
def hash_password(password: str) -> str:
    return bcrypt.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.verify(password, hashed)

# NEVER do this
def bad_hash(password):
    return hashlib.md5(password.encode()).hexdigest()  # WRONG
```

### Session Management
```python
# Secure session configuration
SESSION_CONFIG = {
    'cookie_name': 'session_id',
    'cookie_httponly': True,        # JavaScript cannot access
    'cookie_secure': True,          # HTTPS only
    'cookie_samesite': 'Strict',    # CSRF protection
    'session_timeout': 3600,        # 1 hour
    'renew_on_request': True,       # Reset timeout on each request
}

# NEVER store sensitive data in session
session['user_id'] = user_id  # OK
session['password'] = password  # WRONG
session['credit_card'] = cc_number  # WRONG
```

### Token-Based Auth
```python
# JWT best practices
import jwt
from datetime import datetime, timedelta

JWT_CONFIG = {
    'algorithm': 'RS256',           # Use asymmetric algorithms
    'access_token_expire': 900,    # 15 minutes
    'refresh_token_expire': 86400, # 24 hours
}

# Always verify signatures
def verify_token(token: str) -> dict:
    try:
        # Use public key for RS256
        payload = jwt.decode(
            token,
            public_key,
            algorithms=['RS256']
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthError('Token expired')
    except jwt.InvalidTokenError:
        raise AuthError('Invalid token')

# NEVER do this
payload = jwt.decode(token, 'secret', algorithms=['HS256'])  # Weak
```

## Authorization Checklist

### Role-Based Access Control (RBAC)
```python
# Define roles and permissions
ROLES = {
    'admin': ['read', 'write', 'delete', 'manage_users'],
    'editor': ['read', 'write'],
    'viewer': ['read'],
}

def check_permission(user_role: str, action: str) -> bool:
    return action in ROLES.get(user_role, [])

# Apply in route handlers
@router.get('/users')
@require_permission('read')
def list_users(current_user=Depends(get_current_user)):
    if not check_permission(current_user.role, 'read'):
        raise PermissionDenied()
    return get_users()
```

### Ownership Checks
```python
# Always verify resource ownership
def get_document(doc_id: int, current_user: User):
    doc = db.query(Document).get(doc_id)
    
    # Check ownership
    if doc.owner_id != current_user.id and current_user.role != 'admin':
        raise PermissionDenied('Not your document')
    
    return doc
```

## Input Validation Checklist

### SQL Injection Prevention
```python
# ALWAYS use parameterized queries
def get_user_safe(username: str):
    # GOOD - parameterized
    query = "SELECT * FROM users WHERE username = %s"
    return db.execute(query, (username,))
    
    # BAD - string concatenation
    query = f"SELECT * FROM users WHERE username = '{username}'"  # WRONG
```

### XSS Prevention
```python
# Escape user input before rendering
from markupsafe import escape, Markup

def render_user_content(user_input: str):
    # Escape to prevent XSS
    safe = Markup(escape(user_input))
    return template.render(content=safe)

# For HTML that should allow some tags
from bleach import clean

def sanitize_html(dirty: str):
    return clean(
        dirty,
        tags=['p', 'b', 'i', 'em', 'strong'],
        attributes={},
    )
```

### Command Injection Prevention
```python
import shlex

# NEVER use user input in shell commands
def bad_command(user_input: str):
    os.system(f"echo {user_input}")  # WRONG
    
    # GOOD - use subprocess with list args
    def good_command(user_input: str):
    subprocess.run(['echo', user_input])  # Safe
    
    # If shell=True is needed
    def safe_shell(user_input: str):
        subprocess.run(
            f"echo {shlex.quote(user_input)}",
            shell=True,
            check=True
        )
```

### Path Traversal Prevention
```python
import os
from pathlib import Path

def get_user_file(filename: str):
    base = Path('/safe/directory')
    
    # Resolve and check
    requested = (base / filename).resolve()
    if not requested.is_relative_to(base):
        raise ValueError('Invalid path')
    
    return requested.read_text()
```

## API Security Checklist

### Rate Limiting
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post('/login')
@limiter.limit("5/minute")
async def login(request: Request):
    # Rate limited endpoint
    pass
```

### Input Validation
```python
from pydantic import BaseModel, validator, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 12:
            raise ValueError('Password too short')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Need uppercase')
        if not re.search(r'[0-9]', v):
            raise ValueError('Need number')
        return v
```

### HTTPS Enforcement
```python
# Always redirect HTTP to HTTPS
@app.middleware("http")
async def https_redirect(request: Request, call_next):
    if request.url.scheme == "http":
        url = request.url.replace(scheme="https")
        return RedirectResponse(url)
    return await call_next(request)

# Security headers
@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers['Strict-Transport-Security'] = 'max-age=31536000'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response
```

## Secrets Management Checklist

### Environment Variables
```python
import os

# GOOD - use environment variables
API_KEY = os.environ.get('API_KEY')
if not API_KEY:
    raise ConfigurationError('API_KEY required')

# NEVER hardcode secrets
API_KEY = "sk-1234567890abcdef"  # WRONG
```

### Secrets in Config
```python
# GOOD - use secret management service
from hashicorp_vault import get_secret

API_KEY = get_secret('secret/database', 'api_key')
```

### Logging Sensitive Data
```python
import logging

logger = logging.getLogger(__name__)

# NEVER log sensitive data
logger.info(f"User {username} logged in with password {password}")  # WRONG

# GOOD - log safely
logger.info(f"User {user_id} login attempt")
```

## Payment Security Checklist

### PCI Compliance
```python
# NEVER store card numbers
# Use payment provider (Stripe, PayPal)

# GOOD - use tokenized card
def process_payment(card_token: str, amount: float):
    response = stripe.PaymentIntent.create(
        amount=int(amount * 100),
        currency='usd',
        payment_method=card_token,
        confirm=True,
    )
    return response
```

### Input Validation for Amounts
```python
from decimal import Decimal

def calculate_total(items: list[Item]):
    total = Decimal('0')
    for item in items:
        # Validate price from server
        price = get_product_price(item.product_id)
        total += price * item.quantity
    
    # Verify total
    if total < 0:
        raise ValueError('Invalid total')
    return total
```

## Dependency Security

### Check for Vulnerabilities
```bash
# Python
pip audit
safety check

# JavaScript
npm audit
npm outdated
```

### Keep Dependencies Updated
```yaml
# Dependabot or similar
version: 2
updates:
  - package-ecosystem: pip
    schedule:
      interval: weekly
```

## Security Testing

### Common Vulnerabilities to Test
1. SQL Injection
2. XSS (Cross-Site Scripting)
3. CSRF (Cross-Site Request Forgery)
4. IDOR (Insecure Direct Object References)
5. SSRF (Server-Side Request Forgery)
6. Authentication bypass
7. Authorization bypass
8. Information disclosure

## Constraints

- Never trust user input
- Always validate on server side
- Use parameterized queries
- Implement proper authentication
- Use secure session management
- Keep dependencies updated
- Log security events
- Use HTTPS everywhere
- Never hardcode secrets
