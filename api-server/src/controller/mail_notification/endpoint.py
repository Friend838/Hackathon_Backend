from fastapi import APIRouter

# pylint: disable=import-error
from src.controller.weekly_report.schema.post_weekly_report import (
    PostWeeklyReportRequestBody,
    PostWeeklyReportResponseBody,
)
from src.service.mail_notification_service import MailNotificationService

service = MailNotificationService()

mail_notification_router = APIRouter(prefix="/mailNotify", tags=["Mail notify"])

@mail_notification_router.get(path="/")
async def post_weekly_report():
    await service.simple_send("azsx9015223@gmail.com")
    return 'success'
