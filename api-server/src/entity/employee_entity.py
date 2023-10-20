class Employee:
    def __init__(self, item: dict) -> None:
        self.employ_id: str
        self.zone: str
        self.department: str
        self.shift_time: str

        for k, v in item.items():
            setattr(self, k, v)

    def to_dict(self) -> dict:
        item = vars(self)
        return item
