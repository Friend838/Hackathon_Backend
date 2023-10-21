from camel_converter import dict_to_camel
from camel_converter.pydantic_base import CamelBase


class PostEnterRecordRequestBody(CamelBase):
    employee_id: str
    enter_time: int
    origin_img: str
    labeled_img: str
    target: list[int]
    confidence: list[float]
    position: list[list[float]]
    danger: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                dict_to_camel(
                    {
                        "employee_id": "EMP017",
                        "enter_time": 1694387640,
                        "origin_img": "../images/origin/XXXXXX_XXXXXX.jpg",
                        "labeled_img": "../images/labeled/XXXXXX_XXXXXX.jpg",
                        "target": [1, 1, 2, 2],
                        "confidence": [0.99, 0.99, 0.99, 0.99],
                        "position": [
                            [0.0, 1.1, 2.2, 3.3],
                            [4.4, 5.5, 6.6, 7.7],
                            [8.8, 9.9, 10.10, 11.11],
                            [12.12, 13.13, 14.14, 15.15],
                        ],
                        "danger": 2,
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
