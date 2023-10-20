from camel_converter import dict_to_camel
from camel_converter.pydantic_base import CamelBase


class QueryEmployee(CamelBase):
    employ_id: str
    zone: str
    department: str
    shift_time: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                dict_to_camel(
                    {
                        "employ_id": "EMP030",
                        "zone": "HQ",
                        "department": "DEPT3",
                        "shift_time": "7:30",
                    }
                )
            ]
        }
    }
