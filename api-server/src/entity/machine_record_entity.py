from datetime import datetime

from dateutil import tz


class MachineRecord:
    def __init__(self, item: dict) -> None:
        self.zone: str
        self.timestamp: datetime
        self.tool_scan_time: float

        for k, v in item.items():
            if k == "timestamp":
                setattr(
                    self,
                    k,
                    datetime.fromtimestamp(v, tz=tz.gettz("Asia/Taipei")),
                )
                continue
            setattr(self, k, v)

    def to_dict(self) -> dict:
        item = vars(self)
        item["timestamp"] = int(item["timestamp"].timestamp())
        return item
