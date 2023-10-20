# pylint: disable=import-error
from src.controller.employee.schema.post_employee import (
    PostEmployeeRequestBody,
    PostEmployeeResponseBody,
)
from src.controller.employee.schema.query_employee import QueryEmployee
from src.entity.employee_entity import Employee
from src.infra.repo.employee_repo import EmployeeRepo


class EmployeeService:
    def __init__(self) -> None:
        self.repo = EmployeeRepo()

    def read_employee(self, employ_id: str):
        employee_entity = self.repo.read_employee(employ_id)
        return QueryEmployee(**employee_entity.to_dict())

    def create_employee(self, body: PostEmployeeRequestBody):
        employee_entity = Employee(body.model_dump())
        return PostEmployeeResponseBody(**self.repo.create_employee(employee_entity))
