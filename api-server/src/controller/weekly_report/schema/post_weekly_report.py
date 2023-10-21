from camel_converter import dict_to_camel
from camel_converter.pydantic_base import CamelBase


class PostWeeklyReportRequestBody(CamelBase):
    department: str
    url: str
    timestamp: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                dict_to_camel(
                    {
                        "department": "DEPT1",
                        "url": "https://www.example.com",
                        "timestamp": 1697414400,
                    }
                )
            ]
        }
    }


class PostWeeklyReportResponseBody(CamelBase):
    mongo_object_id: str

    model_config = {
        "json_schema_extra": {"examples": [{"mongo_object_id": "0x00000000000000000"}]}
    }
