from datetime import datetime

from dateutil import tz


class WeeklyReport:
    def __init__(self, item: dict) -> None:
        self.department: str
        self.url: str
        self.timestamp: datetime

        for k, v in item.items():
            if k == "timestamp":
                setattr(self, k, datetime.fromtimestamp(v, tz=tz.gettz("Asia/Taipei")))
                continue
            setattr(self, k, v)

    def to_dict(self) -> dict:
        item = vars(self)
        item["timestamp"] = int(self.timestamp.timestamp())

        return item
