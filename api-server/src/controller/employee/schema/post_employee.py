from camel_converter import dict_to_camel
from camel_converter.pydantic_base import CamelBase


class PostEmployeeRequestBody(CamelBase):
    employ_id: str
    zone: str
    department: str
    shift_time: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                dict_to_camel(
                    {
                        "employ_id": "EMP401",
                        "zone": "HQ",
                        "department": "DEPT1",
                        "shift_time": "7:30",
                    }
                )
            ]
        }
    }


class PostEmployeeResponseBody(CamelBase):
    mongo_object_id: str

    model_config = {
        "json_schema_extra": {"examples": [{"mongo_object_id": "0x00000000000000000"}]}
    }
