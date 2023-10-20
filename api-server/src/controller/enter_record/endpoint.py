from typing import Annotated

from fastapi import APIRouter, Path

# pylint: disable=import-error

enter_record_router = APIRouter(
    prefix="/enterRecord",
    tags=["Enter Record"],
    responses={404: {"description": "Not found"}},
)
