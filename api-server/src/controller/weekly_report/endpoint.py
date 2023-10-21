from fastapi import APIRouter

# pylint: disable=import-error
from src.controller.weekly_report.schema.post_weekly_report import (
    PostWeeklyReportRequestBody,
    PostWeeklyReportResponseBody,
)
from src.service.weekly_report_service import WeeklyReportService

service = WeeklyReportService()

weekly_report_router = APIRouter(prefix="/weeklyReport", tags=["Weekly Report"])


@weekly_report_router.post(path="/", response_model=PostWeeklyReportResponseBody)
def post_weekly_report(body: PostWeeklyReportRequestBody):
    return service.post_weekly_report(body)
