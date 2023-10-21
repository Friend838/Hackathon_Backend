# pylint: disable=import-error
# from src.controller.machine_record.schema.post_machine_record import (
#     PostMachineRecordRequestBody,
#     PostMachineRecordResponseBody,
# )
# from src.controller.machine_record.schema.query_machine_record import QueryMachineRecord
# from src.entity.machine_record_entity import MachineRecord
# from src.infra.repo.machine_record_repo import MachineRecordRepo

from typing import List

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from src.controller.mail_notification.schema.mail_notification import (
    MailNotificationRequestBody,
    MailNotificationResponseBody,
)
from src.dependencies.settings import get_settings


class MailNotificationService:
    def __init__(self):
        setting = get_settings()
        self.conf = ConnectionConfig(
            MAIL_USERNAME=setting.mail_username,
            MAIL_PASSWORD=setting.mail_password,
            MAIL_FROM=setting.mail_from,
            MAIL_PORT=587,
            MAIL_SERVER=setting.mail_server,
            MAIL_FROM_NAME=setting.mail_from_name,
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True,
        )

    async def simple_send(self, body: MailNotificationRequestBody) -> str:
        html = """<p>Hi this test mail, thanks for using Fastapi-mail</p> """
        print(body)
        message = MessageSchema(
            subject=body.email_title,
            recipients=[body.email_to],
            body=body.email_body,
            subtype="html",
        )
        print(message)
        fm = FastMail(self.conf)
        await fm.send_message(message)
        return "success"
