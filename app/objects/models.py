import uuid
from datetime import datetime

from sqlmodel import DateTime, Field, SQLModel, func

# Imported for its side effect as well: `app.models` installs the naming
# convention on the shared SQLModel metadata, which must happen before any table
# class below is defined.
from app.models import get_datetime_utc


class DummyObject(SQLModel, table=True):
    """Fields describe columns, not the API; request and response shapes live in
    `schemas.py`."""

    __tablename__ = "dummy_object"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=255)
    created_at: datetime = Field(
        default_factory=get_datetime_utc,
        nullable=False,
        sa_type=DateTime(timezone=True),  # type: ignore
        sa_column_kwargs={"server_default": func.now()},
    )
