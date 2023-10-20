from camel_converter import dict_to_camel
from camel_converter.pydantic_base import CamelBase


class PostEnterRecordRequestBody(CamelBase):
    employee_id: str
    enter_time: int
    origin_img: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                dict_to_camel(
                    {
                        "employee_id": "EMP017",
                        "enter_time": 1694387640,
                        "origin_img": "/home/user/shot_imgs",
                    }
                )
            ]
        }
    }


class PostEnterRecordResponseBody(CamelBase):
    mongo_object_id: str

    model_config = {
        "json_schema_extra": {"examples": [{"mongo_object_id": "0x00000000000000000"}]}
    }
