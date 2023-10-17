from datetime import datetime
from typing import Any

from dateutil import tz


class User:
    def __init__(self, item: dict) -> None:
        self.id: str
        self.name: str
        self.age: int
        self.birthday: datetime

        for k, v in item.items():
            if k == "birthday":
                v = datetime.fromtimestamp(v, tz=tz.gettz("Asia/Taipei"))
            setattr(self, k, v)

    def to_dict(self) -> dict:
        item = vars(self)
        item["birthday"] = item["birthday"].timestamp()
        return item
