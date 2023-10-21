from camel_converter import dict_to_camel
from camel_converter.pydantic_base import CamelBase

class PostReportMsgRequestBody(CamelBase):
    start_timestamp: int
    end_timestamp: int
    language: str
    type: str
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                dict_to_camel(
                    {
                        "start_timestamp": 1694534400,
                        "end_timestamp": 1695139200,
                        "language": "English",
                        "type": "attandence or machine"
                    }
                )
            ]
        }
    }
    
class PostReportMsgResponseBody(CamelBase):
    title: str
    content: list
    end_timestamp: int
    
    model_config = {
        "json_schema_extra": {"examples": [{"title": "Attendance Weekly Report 9/13/2023 ~ 9/20/2023", "content": ["article1", "article2"], "end_timestamp": 1695139200}]}
    }