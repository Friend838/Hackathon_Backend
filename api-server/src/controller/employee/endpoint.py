from typing import Annotated

from fastapi import APIRouter, Path

# pylint: disable=import-error
from src.controller.employee.schema.post_employee import (
    PostEmployeeRequestBody,
    PostEmployeeResponseBody,
)
from src.controller.employee.schema.query_employee import QueryEmployee
from src.service.employee_service import EmployeeService

employee_router = APIRouter(
    prefix="/Employee",
    tags=["Employee"],
)

service = EmployeeService()


@employee_router.get(
    "/{employ_id}",
    response_model=QueryEmployee,
)
def read_employee(
    employ_id: Annotated[
        str, Path(example="EMP401", description="The ID of employee to get")
    ]
):
    return service.read_employee(employ_id)


@employee_router.post(
    "/",
    response_model=PostEmployeeResponseBody,
)
def creat_employee(body: PostEmployeeRequestBody):
    return service.create_employee(body)
