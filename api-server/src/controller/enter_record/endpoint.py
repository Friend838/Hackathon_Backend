from typing import Annotated

from fastapi import APIRouter, Query
from src.controller.enter_record.schema.get_danger_count import GetDangerCount
from src.controller.enter_record.schema.get_detailed_danger_count import (
    GetDetailedDangerCount,
)

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
    response_model=list[QueryEnterRecord],
)
def get_enter_record(
    start_timestamp: Annotated[int, Query(example=1695225600)],
    end_timestamp: Annotated[int, Query(example=1695312000)],
):
    return service.query_enter_record(start_timestamp, end_timestamp)


@enter_record_router.get(
    path="/totalLateDistributed", response_model=QueryTotalLateDistribution
)
def get_total_late_distributed(
    start_timestamp: Annotated[int, Query(example=1695225600)],
    end_timestamp: Annotated[int, Query(example=1695312000)],
):
    return service.query_total_late_status(start_timestamp, end_timestamp)


@enter_record_router.get(
    path="/departmentLateDistributed",
    response_model=list[QueryLateDistribution],
)
def get_department_late_distributed(
    start_timestamp: Annotated[int, Query(example=1695225600)],
    end_timestamp: Annotated[int, Query(example=1695312000)],
):
    return service.query_department_late_distribution(start_timestamp, end_timestamp)


@enter_record_router.get(
    path="/getDangerCount",
    response_model=GetDangerCount,
)
def get_danger_count(
    start_timestamp: Annotated[int, Query(example=1695225600)],
    end_timestamp: Annotated[int, Query(example=1695312000)],
):
    """
    normal: No abnormal item found
    warning: Electronic device or Notebook found
    danger: Knife or Gun found
    """
    return service.get_danger_count(start_timestamp, end_timestamp)


@enter_record_router.get(
    path="/getDetailedDangerCount", response_model=GetDetailedDangerCount
)
def get_detailed_danger_count(
    start_timestamp: Annotated[int, Query(example=1695225600)],
    end_timestamp: Annotated[int, Query(example=1695312000)],
):
    return service.get_detailed_danger_count(start_timestamp, end_timestamp)
