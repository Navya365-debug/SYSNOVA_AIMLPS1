"""
Security Middleware and Utilities
"""
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, List
import time
import os
from datetime import datetime, timedelta
import jwt


class SecurityMiddleware:
    """Security middleware for API protection."""

    def __init__(self):
        """Initialize security middleware."""
        self.security = HTTPBearer()
        self.jwt_secret = os.getenv("JWT_SECRET_KEY", "your-secret-key")
        self.jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        self.jwt_expiration = int(os.getenv("JWT_EXPIRATION_MINUTES", "30"))

        # Rate limiting
        self.rate_limit_enabled = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"
        self.rate_limit_per_minute = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
        self.request_counts = {}

    async def verify_token(
        self,
        request: Request,
        credentials: HTTPAuthorizationCredentials
    ) -> dict:
        """
        Verify JWT token.

        Args:
            request: FastAPI request
            credentials: HTTP authorization credentials

        Returns:
            Decoded token payload

        Raises:
            HTTPException: If token is invalid
        """
        token = credentials.credentials

        try:
            payload = jwt.decode(
                token,
                self.jwt_secret,
                algorithms=[self.jwt_algorithm]
            )

            # Check expiration
            exp = payload.get("exp")
            if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired"
                )

            return payload

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

    def create_token(
        self,
        user_id: str,
        additional_claims: Optional[dict] = None
    ) -> str:
        """
        Create a JWT token.

        Args:
            user_id: User identifier
            additional_claims: Additional claims to include in token

        Returns:
            JWT token string
        """
        payload = {
            "sub": user_id,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(minutes=self.jwt_expiration),
        }

        if additional_claims:
            payload.update(additional_claims)

        token = jwt.encode(
            payload,
            self.jwt_secret,
            algorithm=self.jwt_algorithm
        )

        return token

    def refresh_token(self, token: str) -> str:
        """
        Refresh an expired token.

        Args:
            token: Expired token

        Returns:
            New JWT token string
        """
        try:
            # Decode without verifying expiration
            payload = jwt.decode(
                token,
                self.jwt_secret,
                algorithms=[self.jwt_algorithm],
                options={"verify_exp": False}
            )

            # Create new token
            user_id = payload.get("sub")
            additional_claims = {k: v for k, v in payload.items()
                               if k not in ["sub", "iat", "exp"]}

            return self.create_token(user_id, additional_claims)

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

    async def check_rate_limit(
        self,
        request: Request,
        user_id: Optional[str] = None
    ) -> bool:
        """
        Check rate limit for a user.

        Args:
            request: FastAPI request
            user_id: User identifier (optional)

        Returns:
            True if request is allowed, False otherwise

        Raises:
            HTTPException: If rate limit is exceeded
        """
        if not self.rate_limit_enabled:
            return True

        # Use user_id or IP address for rate limiting
        identifier = user_id or request.client.host
        current_time = time.time()
        minute = int(current_time / 60)

        # Clean up old entries
        self._cleanup_rate_limits(current_time)

        # Get or create rate limit entry
        if identifier not in self.request_counts:
            self.request_counts[identifier] = {}

        if minute not in self.request_counts[identifier]:
            self.request_counts[identifier][minute] = 0

        # Check rate limit
        if self.request_counts[identifier][minute] >= self.rate_limit_per_minute:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Maximum {self.rate_limit_per_minute} requests per minute."
            )

        # Increment counter
        self.request_counts[identifier][minute] += 1
        return True

    def _cleanup_rate_limits(self, current_time: float):
        """
        Clean up old rate limit entries.

        Args:
            current_time: Current timestamp
        """
        current_minute = int(current_time / 60)
        cutoff_minute = current_minute - 5  # Keep last 5 minutes

        for identifier in list(self.request_counts.keys()):
            for minute in list(self.request_counts[identifier].keys()):
                if minute < cutoff_minute:
                    del self.request_counts[identifier][minute]

            # Remove identifier if no entries left
            if not self.request_counts[identifier]:
                del self.request_counts[identifier]

    def sanitize_input(self, input_string: str) -> str:
        """
        Sanitize user input to prevent injection attacks.

        Args:
            input_string: User input string

        Returns:
            Sanitized string
        """
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&', ';', '|', '`', '$', '(', ')']
        sanitized = input_string

        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')

        return sanitized.strip()

    def validate_email(self, email: str) -> bool:
        """
        Validate email format.

        Args:
            email: Email address

        Returns:
            True if valid, False otherwise
        """
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def validate_password(self, password: str) -> tuple:
        """
        Validate password strength.

        Args:
            password: Password string

        Returns:
            Tuple of (is_valid, error_message)
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"

        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"

        if not any(c.islower() for c in password):
            return False, "Password must contain at least one lowercase letter"

        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one digit"

        return True, ""


class IPWhitelist:
    """IP whitelist for API access control."""

    def __init__(self):
        """Initialize IP whitelist."""
        self.whitelisted_ips = set()
        self.blacklisted_ips = set()

    def add_whitelist(self, ip: str):
        """
        Add IP to whitelist.

        Args:
            ip: IP address
        """
        self.whitelisted_ips.add(ip)

    def add_blacklist(self, ip: str):
        """
        Add IP to blacklist.

        Args:
            ip: IP address
        """
        self.blacklisted_ips.add(ip)

    def is_allowed(self, ip: str) -> bool:
        """
        Check if IP is allowed.

        Args:
            ip: IP address

        Returns:
            True if allowed, False otherwise
        """
        # Check blacklist first
        if ip in self.blacklisted_ips:
            return False

        # If whitelist is not empty, check whitelist
        if self.whitelisted_ips:
            return ip in self.whitelisted_ips

        # If no whitelist, allow all
        return True


# Example usage
if __name__ == "__main__":
    # Create security middleware
    security = SecurityMiddleware()

    # Create token
    token = security.create_token("user123", {"role": "user"})
    print(f"Created token: {token}")

    # Verify token
    try:
        payload = jwt.decode(
            token,
            security.jwt_secret,
            algorithms=[security.jwt_algorithm]
        )
        print(f"Token payload: {payload}")
    except Exception as e:
        print(f"Error: {e}")

    # Sanitize input
    malicious = "<script>alert('xss')</script>"
    safe = security.sanitize_input(malicious)
    print(f"\nSanitized input: {safe}")

    # Validate email
    email = "user@example.com"
    is_valid = security.validate_email(email)
    print(f"Email valid: {is_valid}")

    # Validate password
    password = "SecurePass123"
    is_valid, message = security.validate_password(password)
    print(f"Password valid: {is_valid}, Message: {message}")
