# pylint: disable=import-error
from src.entity.employee_entity import Employee
from src.infra.database.mongo_db import MongoDB


class EmployeeRepo:
    def __init__(self) -> None:
        self.db = MongoDB()
        self.collection_name = "Employee"

    def read_employee(self, employee_id: str):
        document = {"employee_id": employee_id}
        result = self.db.find(self.collection_name, document)

        return Employee(result[0])

    def create_employee(self, employee_entity: Employee):
        payload = employee_entity.to_dict()
        object_id = self.db.insert_one_doc(self.collection_name, payload)
        return {"mongo_object_id": object_id}
