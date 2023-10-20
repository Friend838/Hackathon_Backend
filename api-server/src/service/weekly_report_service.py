# pylint: disable=import-error
from src.controller.weekly_report.schema.post_weekly_report import (
    PostWeeklyReportRequestBody,
    PostWeeklyReportResponseBody,
)
from src.entity.weekly_report_entity import WeeklyReport
from src.infra.repo.weekly_report_repo import WeeklyReportRepo


class WeeklyReportService:
    def __init__(self) -> None:
        self.repo = WeeklyReportRepo()

    def post_weekly_report(
        self, body: PostWeeklyReportRequestBody
    ) -> PostWeeklyReportResponseBody:
        return PostWeeklyReportResponseBody(
            **self.repo.post_weekly_report(WeeklyReport(body.model_dump()))
        )
