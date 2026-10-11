import uuid
from typing import Annotated

from fastapi import Depends

from app.database import SessionDep
from app.objects import service
from app.objects.exceptions import ObjectNotFound
from app.objects.models import DummyObject


def valid_object_id(object_id: uuid.UUID, session: SessionDep) -> DummyObject:
    """Load the object named in the path, or raise 404.

    Every route that takes `{object_id}` reuses this instead of repeating
    the fetch-and-check.
    """
    obj = service.get(session=session, obj_id=object_id)
    if obj is None:
        raise ObjectNotFound()
    return obj


ObjectDep = Annotated[DummyObject, Depends(valid_object_id)]
