from pydantic import BaseModel

# API schemas shared by every domain. Plain Pydantic: SQLModel is reserved for
# table models.


class Message(BaseModel):
    """Generic single-message response."""

    message: str


class ErrorResponse(BaseModel):
    """The body FastAPI returns for a raised `HTTPException`.

    Referenced from route `responses={...}` so failures are documented too.
    """

    detail: str
