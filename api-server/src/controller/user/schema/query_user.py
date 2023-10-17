from datetime import datetime

from camel_converter.pydantic_base import CamelBase


class QueryUser(CamelBase):
    id: str
    name: str
    age: int
    birthday: datetime

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "F123456789",
                    "name": "John",
                    "age": 24,
                    "birthday": "1999-01-01 00:00:00",
                }
            ]
        }
    }
