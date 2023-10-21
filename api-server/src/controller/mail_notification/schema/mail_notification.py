from camel_converter import dict_to_camel
from camel_converter.pydantic_base import CamelBase

class MailNotificationRequestBody(CamelBase):
    email_to: str
    email_title: str
    email_body: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                dict_to_camel(
                    {
                        "email_to": "example@example.com",
                        "email_title": "Warning, dangerous item detected!",
                        "email_body": "Warning, knife object detected!",
                    }
                )
            ]
        }
    }

class MailNotificationResponseBody(CamelBase):
    status: str

    model_config = {
        "json_schema_extra": {"success"}
    }