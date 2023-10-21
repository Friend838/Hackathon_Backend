from camel_converter import dict_to_camel
from camel_converter.pydantic_base import CamelBase


class QueryMachineRecord(CamelBase):
    zone: str
    tool_scan_time: float
    timestamp: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                dict_to_camel(
                    {
                        "zone": "HQ",
                        "tool_scan_time": 0.06,
                        "timestamp": 1670189220,
                    }
                )
            ]
        }
    }
