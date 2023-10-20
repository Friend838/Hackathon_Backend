from datetime import datetime

from dateutil import tz


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
            if k == "enter_time":
                setattr(self, k, datetime.fromtimestamp(v, tz=tz.gettz("Asia/Taipei")))
                continue
            setattr(self, k, v)

    def to_dict(self) -> dict:
        item = vars(self)
        item["enter_time"] = int(item["enter_time"].timestamp())
        return item
