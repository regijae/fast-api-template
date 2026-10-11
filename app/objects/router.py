from typing import Any

from fastapi import APIRouter, Depends, status

from app.auth import dependencies as auth_deps
from app.database import SessionDep
from app.objects import service
from app.objects.dependencies import ObjectDep
from app.objects.schemas import (
    DummyObjectCreate,
    DummyObjectPublic,
    DummyObjectsPublic,
    DummyObjectUpdate,
)
from app.schemas import ErrorResponse, Message

router = APIRouter(
    prefix="/dummy-objects",
    tags=["dummy-objects"],
    dependencies=[Depends(auth_deps.get_current_subject)],
)

NOT_FOUND_RESPONSE: dict[int | str, dict[str, Any]] = {
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorResponse,
        "description": "Dummy object not found",
    },
}

# The handlers below return ORM rows (or a plain dict) and let `response_model`
# validate them exactly once. Do not also build the response model in the body.


@router.get("", response_model=DummyObjectsPublic, summary="List objects")
def list_objects(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    objs, count = service.get_many(session=session, skip=skip, limit=limit)
    return {"data": objs, "count": count}


@router.post(
    "",
    response_model=DummyObjectPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Create an object",
)
def create_object(*, session: SessionDep, obj_in: DummyObjectCreate) -> Any:
    return service.create(session=session, obj_in=obj_in)


@router.get(
    "/{object_id}",
    response_model=DummyObjectPublic,
    summary="Get an object by ID",
    responses=NOT_FOUND_RESPONSE,
)
def get_object(obj: ObjectDep) -> Any:
    return obj


@router.put(
    "/{object_id}",
    response_model=DummyObjectPublic,
    summary="Update an object",
    responses=NOT_FOUND_RESPONSE,
)
def update_object(
    *, session: SessionDep, obj: ObjectDep, obj_in: DummyObjectUpdate
) -> Any:
    return service.update(session=session, db_obj=obj, obj_in=obj_in)


@router.delete(
    "/{object_id}",
    summary="Delete an object",
    responses=NOT_FOUND_RESPONSE,
)
def delete_object(session: SessionDep, obj: ObjectDep) -> Message:
    service.delete(session=session, db_obj=obj)
    return Message(message="Dummy object deleted successfully")
