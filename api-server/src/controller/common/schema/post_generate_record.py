from camel_converter.pydantic_base import CamelBase


class PostGenerateRecord(CamelBase):
    status: str

    model_config = {"json_schema_extra": {"examples": [{"status": "success"}]}}
