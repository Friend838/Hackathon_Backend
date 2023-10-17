from camel_converter.pydantic_base import CamelBase


class PostUserRequestBody(CamelBase):
    id: str
    name: str
    age: int
    birthday: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"id": "A987654321", "name": "Vivian", "age": 23, "birthday": 954086400}
            ]
        }
    }


class PostUserResponseBody(CamelBase):
    mongo_object_id: str

    model_config = {
        "json_schema_extra": {"examples": [{"mongo_object_id": "0x00000000000000000"}]}
    }
