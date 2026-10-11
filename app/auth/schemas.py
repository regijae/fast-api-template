from pydantic import BaseModel


class Token(BaseModel):
    """JSON payload containing an access token."""

    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Contents of a JWT. The subject is the configured API username."""

    sub: str | None = None
