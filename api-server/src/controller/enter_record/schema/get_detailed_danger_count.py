from camel_converter import dict_to_camel
from camel_converter.pydantic_base import CamelBase


class GetDetailedDangerCount(CamelBase):
    electronic_device: int = 0
    laptop: int = 0
    scissor: int = 0
    knife: int = 0
    gun: int = 0

    model_config = {
        "json_schema_extra": {
            "examples": [
                dict_to_camel(
                    {
                        "electronic_device": 0,
                        "laptop": 1,
                        "scissor": 2,
                        "knife": 3,
                        "gun": 4,
                    }
                )
            ]
        }
    }
