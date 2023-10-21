from camel_converter import dict_to_camel
from camel_converter.pydantic_base import CamelBase


class QueryEnterRecord(CamelBase):
    employee_id: str
    zone: str
    shift_time: str
    status: str
