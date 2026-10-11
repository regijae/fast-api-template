import uuid
from collections.abc import Sequence

from sqlmodel import Session, col, func, select

from app.objects.models import DummyObject
from app.objects.schemas import (
    DummyObjectCreate,
    DummyObjectUpdate,
)

# Reference CRUD slice. Copy this shape when adding a real domain.


def create(*, session: Session, obj_in: DummyObjectCreate) -> DummyObject:
    db_obj = DummyObject.model_validate(obj_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get(*, session: Session, obj_id: uuid.UUID) -> DummyObject | None:
    return session.get(DummyObject, obj_id)


def get_many(
    *, session: Session, skip: int = 0, limit: int = 100
) -> tuple[Sequence[DummyObject], int]:
    count_statement = select(func.count()).select_from(DummyObject)
    count = session.exec(count_statement).one()

    statement = (
        select(DummyObject)
        .order_by(col(DummyObject.created_at).desc())
        .offset(skip)
        .limit(limit)
    )
    objs = session.exec(statement).all()

    return objs, count


def update(
    *,
    session: Session,
    db_obj: DummyObject,
    obj_in: DummyObjectUpdate,
) -> DummyObject:
    db_obj.sqlmodel_update(obj_in.model_dump(exclude_unset=True))
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def delete(*, session: Session, db_obj: DummyObject) -> None:
    session.delete(db_obj)
    session.commit()
