# pylint: disable=import-error
from src.controller.employee.schema.post_employee import (
    PostEmployeeRequestBody,
    PostEmployeeResponseBody,
)
from src.controller.employee.schema.query_employee import QueryEmployee
from src.controller.employee.schema.query_employee_distribution import (
    DepartmentEmployeeNumber,
    QueryEmployeeDistribution,
)
from src.entity.employee_entity import Employee
from src.infra.repo.employee_repo import EmployeeRepo


class EmployeeService:
    def __init__(self) -> None:
        self.repo = EmployeeRepo()

    def read_employee(self, employee_id: str):
        employee_entity = self.repo.read_employee(employee_id)
        return QueryEmployee(**employee_entity.to_dict())

    def create_employee(self, body: PostEmployeeRequestBody):
        employee_entity = Employee(body.model_dump())
        return PostEmployeeResponseBody(**self.repo.create_employee(employee_entity))
    
    def get_distribution(self):
        employee_entity_list = self.repo.read_all_employee()
        
        counting_result = {
            "HQ": {
                "DEPT1": 0,
                "DEPT2": 0,
                "DEPT3": 0,
                "DEPT4": 0,
            },
            "AZ": {
                "DEPT1": 0,
                "DEPT2": 0,
                "DEPT3": 0,
                "DEPT4": 0,
            }
        }
        
        for entity in employee_entity_list:
            counting_result[entity.zone][entity.department] += 1
        
        
        response = [
            QueryEmployeeDistribution(
                zone="HQ",
                departments=[
                    DepartmentEmployeeNumber(
                        department=key,
                        number=counting_result["HQ"][key]
                    )
                    for key in counting_result["HQ"]
                ]
            ),
            QueryEmployeeDistribution(
                zone="AZ",
                departments=[
                    DepartmentEmployeeNumber(
                        department=key,
                        number=counting_result["AZ"][key]
                    )
                    for key in counting_result["AZ"]
                ]
            ),
        ]
        
        return response

