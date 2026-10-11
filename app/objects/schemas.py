import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

# The client-facing contract. Plain Pydantic.


class DummyObjectCreate(BaseModel):
    """Properties to receive on creation."""

    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


class DummyObjectUpdate(BaseModel):
    """Properties to receive on update, all optional."""

    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


class DummyObjectPublic(BaseModel):
    """Properties to return via the API."""

    id: uuid.UUID
    title: str
    description: str | None = None
    created_at: datetime


class DummyObjectsPublic(BaseModel):
    data: list[DummyObjectPublic]
    count: int
