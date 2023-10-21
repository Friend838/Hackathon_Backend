from camel_converter import dict_to_camel
from camel_converter.pydantic_base import CamelBase


class GetDangerCount(CamelBase):
    normal: int = 0
    warning: int = 0
    danger: int = 0