# pylint: disable=import-error
from camel_converter import dict_to_camel
from camel_converter.pydantic_base import CamelBase


class QueryTotalLateDistribution(CamelBase):
    the_number_of_late: int
    the_number_of_on_time: int
    the_number_of_early: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                dict_to_camel(
                    {
                        "the_number_of_late": 1,
                        "the_number_of_on_time": 2,
                        "the_number_of_early": 3,
                    }
                )
            ]
        }
    }
    
    def asDict(self):
        return {"late": self.the_number_of_late, "on_time": self.the_number_of_on_time, "early": self.the_number_of_early}
