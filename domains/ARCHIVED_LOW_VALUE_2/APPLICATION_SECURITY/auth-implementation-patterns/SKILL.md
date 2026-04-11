---
name: auth-implementation-patterns
description: "Use when: implementing authentication and authorization systems, building secure login flows, setting up JWT or session management, or configuring RBAC. Triggers: 'auth', 'authentication', 'authorization', 'login', 'JWT', 'OAuth', 'session', 'RBAC', 'permissions', 'access control', 'sign in', 'sign up'. NOT for: public read-only APIs without user context, or when using external auth providers without customization."
---

# Auth Implementation Patterns

Master authentication and authorization patterns including JWT, OAuth2, session management, and RBAC to build secure, scalable access control systems.

## When to Use This Skill

Use this skill when:
- Implementing authentication from scratch
- Setting up JWT or OAuth2 authentication
- Building session management
- Configuring role-based access control (RBAC)
- Securing API endpoints
- Debugging auth issues

Do NOT use when:
- Using fully managed auth (Auth0, Clerk without customization)
- Public read-only APIs without user context
- Simple internal tools without security requirements

## Authentication Methods Comparison

| Method | Best For | Tokens | Complexity |
|--------|----------|--------|------------|
| **JWT** | APIs, SPAs | Stateless | Medium |
| **Session** | Traditional web apps | Stateful | Low |
| **OAuth2** | Third-party logins | Varies | High |
| **API Keys | Service-to-service | Static | Low |

## JWT Implementation

### Token Structure
```python
import jwt
from datetime import datetime, timedelta
from typing import Optional

class JWTManager:
    def __init__(self, public_key_path: str, private_key_path: str):
        with open(private_key_path) as f:
            self.private_key = f.read()
        with open(public_key_path) as f:
            self.public_key = f.read()
    
    def create_access_token(
        self,
        subject: str,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        
        to_encode = {
            "sub": subject,
            "exp": expire,
            "type": "access"
        }
        
        return jwt.encode(
            to_encode,
            self.private_key,
            algorithm="RS256"
        )
    
    def create_refresh_token(self, subject: str) -> str:
        expire = datetime.utcnow() + timedelta(days=30)
        to_encode = {
            "sub": subject,
            "exp": expire,
            "type": "refresh"
        }
        
        return jwt.encode(
            to_encode,
            self.private_key,
            algorithm="RS256"
        )
    
    def verify_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                self.public_key,
                algorithms=["RS256"]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError()
        except jwt.InvalidTokenError:
            raise InvalidTokenError()
```

### FastAPI Integration
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    jwt_manager: JWTManager = Depends(get_jwt_manager)
) -> User:
    token = credentials.credentials
    
    try:
        payload = jwt_manager.verify_token(token)
        user_id = payload.get("sub")
        
        if user_id is None:
            raise InvalidTokenError()
        
        user = await get_user_by_id(user_id)
        if user is None:
            raise UserNotFoundError()
        
        return user
        
    except TokenExpiredError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Protected route
@router.get("/users/me")
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    return current_user
```

## Session Management

### Redis-Backed Sessions
```python
import redis
import json
from datetime import timedelta
from uuid import uuid4

class SessionManager:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
    
    def create_session(
        self,
        user_id: str,
        data: dict,
        ttl_seconds: int = 3600
    ) -> str:
        session_id = str(uuid4())
        
        session_data = {
            "user_id": user_id,
            **data
        }
        
        key = f"session:{session_id}"
        self.redis.setex(
            key,
            ttl_seconds,
            json.dumps(session_data)
        )
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[dict]:
        key = f"session:{session_id}"
        data = self.redis.get(key)
        
        if data:
            return json.loads(data)
        return None
    
    def refresh_session(self, session_id: str, ttl_seconds: int = 3600):
        key = f"session:{session_id}"
        self.redis.expire(key, ttl_seconds)
    
    def destroy_session(self, session_id: str):
        key = f"session:{session_id}"
        self.redis.delete(key)
```

### Secure Cookie Configuration
```python
from fastapi import Response

def set_session_cookie(response: Response, session_id: str):
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,        # JavaScript cannot access
        secure=True,           # HTTPS only
        samesite="strict",    # CSRF protection
        max_age=3600,          # 1 hour
        path="/",
    )

def clear_session_cookie(response: Response):
    response.delete_cookie(
        key="session_id",
        path="/",
    )
```

## OAuth2 Implementation

### OAuth2 Flow
```python
from urllib.parse import urlencode

class OAuth2Provider:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        auth_url: str,
        token_url: str,
        userinfo_url: str
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.auth_url = auth_url
        self.token_url = token_url
        self.userinfo_url = userinfo_url
    
    def get_authorization_url(self, state: str) -> str:
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": "openid profile email",
            "state": state,
        }
        return f"{self.auth_url}?{urlencode(params)}"
    
    def exchange_code_for_token(self, code: str) -> dict:
        response = requests.post(
            self.token_url,
            data={
                "grant_type": "authorization_code",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": code,
                "redirect_uri": self.redirect_uri,
            }
        )
        return response.json()
    
    def get_user_info(self, access_token: str) -> dict:
        response = requests.get(
            self.userinfo_url,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        return response.json()
```

### Google OAuth Example
```python
google_oauth = OAuth2Provider(
    client_id=os.environ["GOOGLE_CLIENT_ID"],
    client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
    redirect_uri="https://app.com/auth/google/callback",
    auth_url="https://accounts.google.com/o/oauth2/v2/auth",
    token_url="https://oauth2.googleapis.com/token",
    userinfo_url="https://www.googleapis.com/oauth2/v3/userinfo",
)

@router.get("/auth/google")
async def google_login():
    state = generate_secure_state()
    # Store state in session for verification
    url = google_oauth.get_authorization_url(state)
    return RedirectResponse(url)

@router.get("/auth/google/callback")
async def google_callback(code: str, state: str):
    # Verify state matches
    token_data = google_oauth.exchange_code_for_token(code)
    user_info = google_oauth.get_user_info(token_data["access_token"])
    
    # Create or find user
    user = await get_or_create_user(
        provider="google",
        provider_id=user_info["sub"],
        email=user_info["email"],
        name=user_info.get("name"),
    )
    
    # Create app session
    return create_session(user)
```

## RBAC Implementation

### Role Definitions
```python
from enum import Enum
from typing import Set

class Role(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"

class Permission(str, Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    MANAGE_USERS = "manage_users"

ROLE_PERMISSIONS: dict[Role, Set[Permission]] = {
    Role.ADMIN: {
        Permission.READ,
        Permission.WRITE,
        Permission.DELETE,
        Permission.MANAGE_USERS,
    },
    Role.EDITOR: {
        Permission.READ,
        Permission.WRITE,
    },
    Role.VIEWER: {
        Permission.READ,
    },
}
```

### Permission Checker
```python
from functools import wraps
from fastapi import HTTPException, status

def require_permission(permission: Permission):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs):
            user_permissions = ROLE_PERMISSIONS.get(current_user.role, set())
            
            if permission not in user_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Missing permission: {permission}"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Usage
@router.delete("/documents/{doc_id}")
@require_permission(Permission.DELETE)
async def delete_document(
    doc_id: int,
    current_user: User = Depends(get_current_user)
):
    # Only admins can delete
    return await delete(doc_id)
```

### Resource-Level Authorization
```python
async def check_document_access(
    user: User,
    document: Document,
    required_permission: Permission
) -> bool:
    # Admin has full access
    if user.role == Role.ADMIN:
        return True
    
    # Check if user owns the document
    if document.owner_id == user.id:
        return True
    
    # Check group permissions
    if document.group_id in user.groups:
        return True
    
    return False
```

## Multi-Factor Authentication

### TOTP Implementation
```python
import pyotp

class TOTPManager:
    def generate_secret(self) -> str:
        return pyotp.random_base32()
    
    def get_provisioning_uri(self, secret: str, email: str) -> str:
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(
            name=email,
            issuer_name="MyApp"
        )
    
    def verify(self, secret: str, token: str) -> bool:
        totp = pyotp.TOTP(secret)
        return totp.verify(token)
```

### Login Flow with MFA
```python
async def login_with_mfa(username: str, password: str, mfa_code: str = None):
    user = await authenticate_user(username, password)
    
    if not user:
        raise InvalidCredentialsError()
    
    if user.mfa_enabled:
        if not mfa_code:
            raise MFARequiredError()
        
        if not totp_manager.verify(user.mfa_secret, mfa_code):
            raise InvalidMFAError()
    
    return create_session(user)
```

## Constraints

- Use strong password hashing (bcrypt, argon2)
- Implement proper token expiration
- Use HTTPS for all auth flows
- Validate redirect URIs in OAuth
- Implement account lockout after failed attempts
- Use secure session cookies (HttpOnly, Secure, SameSite)
- Rotate secrets regularly
- Log authentication events
- Implement MFA for sensitive accounts
- Never store passwords in plain text
