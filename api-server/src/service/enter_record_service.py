from datetime import datetime, timedelta

# pylint: disable=import-error
from src.controller.enter_record.schema.post_enter_record import (
    PostEnterRecordRequestBody,
    PostEnterRecordResponseBody,
)
from src.controller.enter_record.schema.query_enter_record import QueryEnterRecord
from src.controller.enter_record.schema.query_late_distribution import (
    DepartmentLateDistribution,
    QueryLateDistribution,
)
from src.controller.enter_record.schema.query_total_late_distribution import (
    QueryTotalLateDistribution,
)
from src.controller.enter_record.schema.get_danger_count import GetDangerCount
from src.entity.enter_record_entity import EnterRecord
from src.infra.repo.enter_record_repo import EnterRecordRepo
from src.service.employee_service import EmployeeService


class EnterRecordService:
    def __init__(self) -> None:
        self.repo = EnterRecordRepo()
        self.employee_service = EmployeeService()

    def process_enter_record(self, body: PostEnterRecordRequestBody):
        enter_record_entity = EnterRecord(body.model_dump())

        enter_record_entity.labeled_img = "TBA"
        enter_record_entity.target = "TBA"
        enter_record_entity.confidence = "TBA"
        enter_record_entity.position = "TBA"
        enter_record_entity.danger = "TBA"

        return PostEnterRecordResponseBody(
            **self.repo.post_enter_record(enter_record_entity)
        )

    def query_enter_record(self, start_timestamp: int, end_timestamp: int):
        entity_list = self.repo.get_enter_record(start_timestamp, end_timestamp)

        result_list = []
        for entity in entity_list:
            employee_entity = self.employee_service.read_employee(
                employee_id=entity.employee_id
            )
            shift_time = datetime.strptime("%H:%M", employee_entity.shift_time)

            if shift_time < entity.enter_time.time():
                status = "late"
            elif (
                shift_time - timedelta(minutes=20)
                <= entity.enter_time.time()
                <= shift_time
            ):
                status = "on-time"
            else:
                status = "early"

            result_list.append(
                QueryEnterRecord(
                    employee_id=employee_entity.employee_id,
                    zone=employee_entity.zone,
                    shift_time=employee_entity.shift_time,
                    status=status,
                )
            )

    def query_total_late_status(self, start_timestamp: int, end_timestamp: int):
        entity_list = self.repo.get_enter_record(start_timestamp, end_timestamp)

        result_dict = {"late": 0, "on-time": 0, "early": 0}
        for entity in entity_list:
            employee_entity = self.employee_service.read_employee(
                employee_id=entity.employee_id
            )
            shift_time = datetime.strptime("%H:%M", employee_entity.shift_time)

            if shift_time < entity.enter_time.time():
                result_dict["late"] += 1
            elif (
                shift_time - timedelta(minutes=20)
                <= entity.enter_time.time()
                <= shift_time
            ):
                result_dict["on-time"] += 1
            else:
                result_dict["early"] += 1

        return QueryTotalLateDistribution(
            the_number_of_late=result_dict["late"],
            the_number_of_on_time=result_dict["on-time"],
            the_number_of_early=result_dict["early"],
        )

    def query_department_late_distribution(
        self, start_timestamp: int, end_timestamp: int
    ):
        entity_list = self.repo.get_enter_record(start_timestamp, end_timestamp)
        department_in_zone = {"HQ": {}, "AZ": {}}

        for entity in entity_list:
            employee_entity = self.employee_service.read_employee(
                employee_id=entity.employee_id
            )
            if (
                employee_entity.department
                not in department_in_zone[employee_entity.zone]
            ):
                department_in_zone[employee_entity.zone][employee_entity.department] = {
                    "early": 0,
                    "on-time": 0,
                    "late": 0,
                }

            shift_time = datetime.strptime("%H:%M", employee_entity.shift_time)

            if shift_time < entity.enter_time.time():
                department_in_zone[employee_entity.zone][employee_entity.department][
                    "late"
                ] += 1
            elif (
                shift_time - timedelta(minutes=20)
                <= entity.enter_time.time()
                <= shift_time
            ):
                department_in_zone[employee_entity.zone][employee_entity.department][
                    "on_time"
                ] += 1
            else:
                department_in_zone[employee_entity.zone][employee_entity.department][
                    "early"
                ] += 1

        result = [
            QueryLateDistribution(
                zone="HQ",
                late_distribution=[
                    DepartmentLateDistribution(
                        department=dept,
                        the_number_of_late=department_in_zone["HQ"][dept]["late"],
                        the_number_of_on_time=department_in_zone["HQ"][dept]["on-time"],
                        the_number_of_early=department_in_zone["HQ"][dept]["early"],
                    )
                    for dept in department_in_zone["HQ"]
                ],
            ),
            QueryLateDistribution(
                zone="AZ",
                late_distribution=[
                    DepartmentLateDistribution(
                        department=dept,
                        the_number_of_late=department_in_zone["AZ"][dept]["late"],
                        the_number_of_on_time=department_in_zone["AZ"][dept]["on-time"],
                        the_number_of_early=department_in_zone["AZ"][dept]["early"],
                    )
                    for dept in department_in_zone["AZ"]
                ],
            ),
        ]

        return result
    
    def get_danger_count(self, start_timestamp: int, end_timestamp: int):
        entity_list = self.repo.get_enter_record(start_timestamp, end_timestamp)
        getDangerCount = [0, 0, 0]
        print(entity_list)
        for entity in entity_list:
            if entity.danger == 'Normal':
                getDangerCount[0] += 1
            elif entity.danger == 'Warning':
                getDangerCount[1] += 1
            elif entity.danger == 'Danger':
                getDangerCount[2] += 1

        return GetDangerCount(
            normal=getDangerCount[0],
            warning=getDangerCount[1],
            danger=getDangerCount[2]
        )
