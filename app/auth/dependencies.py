from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.auth import service
from app.auth.config import auth_settings
from app.auth.exceptions import InvalidToken
from app.config import settings

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_subject(token: TokenDep) -> str:
    """Validate the bearer token and return its subject - the API username."""
    token_data = service.decode_token(token)
    if token_data.sub is None or token_data.sub != auth_settings.API_USERNAME:
        raise InvalidToken()
    return token_data.sub


CurrentSubject = Annotated[str, Depends(get_current_subject)]
