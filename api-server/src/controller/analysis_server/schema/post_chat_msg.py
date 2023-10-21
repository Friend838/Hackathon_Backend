from camel_converter import dict_to_camel
from camel_converter.pydantic_base import CamelBase

class PostChatMsgRequestBody(CamelBase):
    message: str
    language: str
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                dict_to_camel(
                    {
                        "message": "How many people late today",
                        "language": "English",
                    }
                )
            ]
        }
    }
    
class PostChatMsgResponseBody(CamelBase):
    message: str
    
    model_config = {
        "json_schema_extra": {"examples": [{"message": "5 people late today"}]}
    }