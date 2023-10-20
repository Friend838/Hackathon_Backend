from fastapi import APIRouter, Path

# pylint: disable=import-error
from src.controller.enter_record.schema.post_enter_record import (
    PostEnterRecordRequestBody,
    PostEnterRecordResponseBody,
)
from src.service.enter_record_service import EnterRecordService

service = EnterRecordService()

enter_record_router = APIRouter(
    prefix="/enterRecord",
    tags=["Enter Record"],
)


@enter_record_router.post(
    path="/",
    response_model=PostEnterRecordResponseBody,
)
def generate_enter_record(
    body: PostEnterRecordRequestBody,
):
    return service.process_enter_record(body)
