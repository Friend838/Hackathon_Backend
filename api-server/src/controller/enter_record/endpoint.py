from typing import Annotated

from fastapi import APIRouter, Query

# pylint: disable=import-error
from src.controller.enter_record.schema.post_enter_record import (
    PostEnterRecordRequestBody,
    PostEnterRecordResponseBody,
)
from src.controller.enter_record.schema.query_enter_record import QueryEnterRecord
from src.controller.enter_record.schema.query_late_distribution import (
    QueryLateDistribution,
)
from src.controller.enter_record.schema.query_total_late_distribution import (
    QueryTotalLateDistribution,
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


@enter_record_router.get(
    path="/",
    response_model=QueryEnterRecord,
)
def get_enter_record(
    start_timestamp: Annotated[int, Query(example=0)],
    end_timestamp: Annotated[int, Query(example=0)],
):
    return service.query_enter_record(start_timestamp, end_timestamp)


@enter_record_router.get(
    path="/totalLateDistributed", response_model=QueryTotalLateDistribution
)
def get_total_late_distributed(
    start_timestamp: Annotated[int, Query(example=0)],
    end_timestamp: Annotated[int, Query(example=0)],
):
    return service.query_total_late_status(start_timestamp, end_timestamp)


@enter_record_router.get(
    path="/departmentLateDistributed",
    response_model=QueryLateDistribution,
)
def get_department_late_distributed(
    start_timestamp: Annotated[int, Query(example=0)],
    end_timestamp: Annotated[int, Query(example=0)],
):
    return service.query_department_late_status(start_timestamp, end_timestamp)
