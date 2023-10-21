from datetime import datetime

from dateutil import tz


class EnterRecord:
    def __init__(self, item: dict) -> None:
        self.employee_id: str
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
    
    def brief() -> str:
        return (
            "employee_id: The employee id of the employee (String),\n"
            "enter_time: The timestamp of the employee entering the office, for example 1694387640 (Number),\n"
            "origin_img: The x-ray image's path of the employee's belongings (String),\n"
            "label_img: The labeled x-ray image's path of the orgin_img (String),\n"
            "target: The identified contraband in the origin_img (list of String),\n"
            "confidence: The confidence value of each contraband be identified in the origin_img (list of Number),\n"
            "position: The position of each contraband (list of list of 4 Number),\n"
            "danger: The danger level of the identified contrabands, normal, warning, or danger (String)\n"
        )