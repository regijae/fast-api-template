from app.auth.constants import ErrorCode
from app.exceptions import BadRequest, NotAuthenticated


class InvalidCredentials(BadRequest):
    """The username/password posted to the login endpoint did not match."""

    DETAIL = ErrorCode.INVALID_CREDENTIALS


class InvalidToken(NotAuthenticated):
    """The bearer token is missing, malformed, expired, or for another subject."""

    DETAIL = ErrorCode.INVALID_TOKEN
