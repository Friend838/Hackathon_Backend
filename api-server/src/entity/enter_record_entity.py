from datetime import datetime
from enum import Enum


class Danger(Enum):
    type_0: "正常"
    type_1: "警告"
    type_2: "危險"


class EnterRecord:
    def __init__(self, item: dict) -> None:
        self.employ_id: str
        self.enter_time: datetime
        self.origin_img: str
        self.labeled_img: str
        self.target: list[str]
        self.confidence: list[float]
        self.position: list[tuple]
        self.danger: str

        for k, v in item.items():
            setattr(self, k, v)

    def to_dict(self) -> dict:
        return vars(self)
