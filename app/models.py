from datetime import UTC, datetime

from sqlmodel import SQLModel

# Applied to the shared SQLModel metadata before any table class is imported, so
# indexes, constraints and foreign keys get predictable names instead of whatever
# PostgreSQL happens to assign. Only affects objects created from here on; the
# existing primary key already resolves to `dummy_object_pkey`.
POSTGRES_INDEXES_NAMING_CONVENTION: dict[str, str] = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}
SQLModel.metadata.naming_convention = POSTGRES_INDEXES_NAMING_CONVENTION


def get_datetime_utc() -> datetime:
    """Timezone-aware `now`, for model defaults."""
    return datetime.now(UTC)
