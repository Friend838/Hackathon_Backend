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
    
    def brief() -> str:
        return (
            "zone: The zone of the machine, either \"HQ\" or \"AZ\" (String),\n"
            "timestamp: The timestamp when the machine is scanning, for example 1694388540 (Number),\n"
            "tool_scan_time: The duration of the machine scanning, for example 0.87 (Number)"
        )
