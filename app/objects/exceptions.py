from app.exceptions import NotFound
from app.objects.constants import ErrorCode


class ObjectNotFound(NotFound):
    DETAIL = ErrorCode.OBJECT_NOT_FOUND
