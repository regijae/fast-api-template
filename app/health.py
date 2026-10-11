"""Liveness and readiness probes."""

import logging
from typing import Literal

from fastapi import APIRouter, Response, status
from pydantic import BaseModel
from sqlmodel import text

from app.database import engine

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["health"])


class Health(BaseModel):
    status: Literal["ok", "error"]


@router.get("/live", summary="Liveness probe")
def live(response: Response) -> Health:
    response.headers["Cache-Control"] = "no-store"
    return Health(status="ok")


@router.get(
    "/ready",
    summary="Readiness probe",
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "model": Health,
            "description": "A backing service is unavailable",
        },
    },
)
def ready(response: Response) -> Health:
    response.headers["Cache-Control"] = "no-store"
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception:
        logger.warning("Readiness probe failed: database unreachable", exc_info=True)
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return Health(status="error")

    return Health(status="ok")
