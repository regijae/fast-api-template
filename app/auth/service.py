import secrets
from datetime import UTC, datetime, timedelta

import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError

from app.auth.config import auth_settings
from app.auth.exceptions import InvalidToken
from app.auth.schemas import TokenPayload


def verify_credentials(username: str, password: str) -> bool:
    """Check the submitted credentials against the configured ones."""

    username_ok = secrets.compare_digest(username, auth_settings.API_USERNAME)
    password_ok = secrets.compare_digest(password, auth_settings.API_PASSWORD)
    return username_ok and password_ok


def create_access_token(subject: str) -> str:
    expire = datetime.now(UTC) + timedelta(
        minutes=auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return jwt.encode(
        {"exp": expire, "sub": subject},
        auth_settings.SECRET_KEY,
        algorithm=auth_settings.JWT_ALG,
    )


def decode_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(
            token, auth_settings.SECRET_KEY, algorithms=[auth_settings.JWT_ALG]
        )
        return TokenPayload(**payload)
    except (InvalidTokenError, ValidationError) as exc:
        raise InvalidToken() from exc
