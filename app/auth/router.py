from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import service
from app.auth.config import auth_settings
from app.auth.exceptions import InvalidCredentials
from app.auth.schemas import Token
from app.schemas import ErrorResponse

router = APIRouter(tags=["login"])


@router.post(
    "/login/access-token",
    summary="Exchange credentials for an access token",
    description=(
        "OAuth2 compatible token login. Post the configured API_USERNAME and "
        "API_PASSWORD to get a bearer token for the protected routes."
    ),
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": "Incorrect username or password",
        },
    },
)
def login_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    if not service.verify_credentials(form_data.username, form_data.password):
        raise InvalidCredentials()
    return Token(access_token=service.create_access_token(auth_settings.API_USERNAME))
