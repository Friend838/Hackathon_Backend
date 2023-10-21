from camel_converter import dict_to_camel
from camel_converter.pydantic_base import CamelBase


class DepartmentLateDistribution(CamelBase):
    department: str
    the_number_of_late: int
    the_number_of_on_time: int
    the_number_of_early: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                dict_to_camel(
                    {
                        "department": "DEPT1",
                        "the_number_of_early": 1,
                        "the_number_of_on_time": 2,
                        "the_number_of_late": 3,
                    }
                )
            ]
        }
    }


class QueryLateDistribution(CamelBase):
    zone: str
    late_distribution: list[DepartmentLateDistribution]

    model_config = {
        "json_schema_extra": {
            "examples": [
                dict_to_camel(
                    {
                        "zone": "AZ",
                        "late_distribution": [
                            DepartmentLateDistribution(
                                department="DEPT1",
                                the_number_of_late=1,
                                the_number_of_on_time=2,
                                the_number_of_early=3,
                            ).model_dump(),
                            DepartmentLateDistribution(
                                department="DEPT2",
                                the_number_of_late=3,
                                the_number_of_on_time=2,
                                the_number_of_early=1,
                            ).model_dump(),
                        ],
                    }
                )
            ]
        }
    }
