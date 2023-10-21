class Employee:
    def __init__(self, item: dict) -> None:
        self.employee_id: str
        self.zone: str
        self.department: str
        self.shift_time: str

        for k, v in item.items():
            setattr(self, k, v)

    def to_dict(self) -> dict:
        item = vars(self)
        return item

    def brief() -> str:
        return (
            "employee_id: The uuid of employee, for example Emp001 (String),\n"
            "zone: The zone of employee, either \"HQ\" or \"AZ\" (String),\n"
            "department: The department of employee, from \"DEPT1\ to \"DEPT4\" (String),\n"
            "shift_time: The time that the employee should arrive before, for example 7:30 (String)"
        )