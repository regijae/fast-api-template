from enum import StrEnum


class ErrorCode(StrEnum):
    INVALID_CREDENTIALS = "Incorrect username or password"
    INVALID_TOKEN = "Could not validate credentials"
