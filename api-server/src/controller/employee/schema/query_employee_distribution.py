from camel_converter import dict_to_camel
from camel_converter.pydantic_base import CamelBase


class DepartmentEmployeeNumber(CamelBase):
    department: str
    number: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "department": "DEPT1",
                    "number": 20
                }
            ]
        }
    }

class QueryEmployeeDistribution(CamelBase):
    zone: str
    departments: list[DepartmentEmployeeNumber]

    model_config = {
        "json_schema_extra": {
            "examples": [
                dict_to_camel(
                    {
                        "zone": "HQ",
                        "departments": [
                            DepartmentEmployeeNumber(
                                department="DEPT1",
                                number=20
                            ).model_dump(),
                            DepartmentEmployeeNumber(
                                department="DEPT1",
                                number=100
                            ).model_dump(),
                        ]
                    }
                )
            ]
        }
    }
