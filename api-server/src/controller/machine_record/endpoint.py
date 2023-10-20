from fastapi import APIRouter, Path

# pylint: disable=import-error
from src.controller.machine_record.schema.post_machine_record import (
    PostMachineRecordRequestBody,
    PostMachineRecordResponseBody,
)
from src.service.machine_record_service import MachineRecordService

service = MachineRecordService()

machine_record_router = APIRouter(
    prefix="/machineRecord",
    tags=["Machine Record"],
)


@machine_record_router.post(
    path="/",
    response_model=PostMachineRecordResponseBody,
)
def generate_machine_record(
    body: PostMachineRecordRequestBody,
):
    return service.post_machine_record(body)
