from fastapi import APIRouter

# pylint: disable=import-error
from src.controller.mail_notification.schema.mail_notification import (
    MailNotificationRequestBody,
    MailNotificationResponseBody,
)

from src.service.mail_notification_service import MailNotificationService

service = MailNotificationService()

mail_notification_router = APIRouter(prefix="/mailNotify", tags=["Mail notify"])

@mail_notification_router.post(
        path="/caution",
        response_model=MailNotificationResponseBody
)
async def mail_notification(body: MailNotificationRequestBody):
    await service.simple_send(body)
    return MailNotificationResponseBody(status='success')
