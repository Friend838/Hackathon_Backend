from camel_converter import dict_to_camel
from camel_converter.pydantic_base import CamelBase


class QueryEnterRecord(CamelBase):
    employee_id: str
    zone: str
    department: str
    shift_time: str
    status: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                dict_to_camel(
                    {
                        "employee_id": "EMP017",
                        "zone": "HQ",
                        "department": "DEPT4",
                        "shift_time": "7:30",
                        "status": "on-time",
                    }
                )
            ]
        }
    }
