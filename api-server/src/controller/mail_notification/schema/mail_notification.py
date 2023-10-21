from camel_converter import dict_to_camel
from camel_converter.pydantic_base import CamelBase

class MailNotificationRequestBody(CamelBase):
    zone: str
    tool_scan_time: float
    timestamp: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                dict_to_camel(
                    {
                        "zone": "HQ",
                        "tool_scan_time": 0.06,
                        "timestamp": 1670189220,
                    }
                )
            ]
        }
    }


class MailNotificationResponseBody(CamelBase):
    mongo_object_id: str

    model_config = {
        "json_schema_extra": {"examples": [{"mongo_object_id": "0x00000000000000000"}]}
    }