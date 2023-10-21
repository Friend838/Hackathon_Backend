from fastapi import APIRouter, Query
from typing import Annotated

# pylint: disable=import-error
from src.controller.machine_record.schema.post_machine_record import (
    PostMachineRecordRequestBody,
    PostMachineRecordResponseBody,
)
from src.controller.machine_record.schema.query_machine_record import QueryMachineRecord
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


@machine_record_router.get(
    path="/",
    response_model=list[QueryMachineRecord],
)
def query_machine_record(
    start_timestamp: Annotated[int, Query(gt=0, example=None)],
    end_timestamp: Annotated[int, Query(gt=0, example=None)],
):
    return service.get_machine_record(start_timestamp, end_timestamp)
