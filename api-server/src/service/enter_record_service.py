from datetime import datetime

# pylint: disable=import-error
from src.controller.enter_record.schema.post_enter_record import (
    PostEnterRecordRequestBody,
    PostEnterRecordResponseBody,
)
from src.controller.enter_record.schema.query_enter_record import QueryEnterRecord
from src.entity.enter_record_entity import EnterRecord
from src.infra.repo.enter_record_repo import EnterRecordRepo
from src.service.employee_service import EmployeeService


class EnterRecordService:
    def __init__(self) -> None:
        self.repo = EnterRecordRepo()

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

        employee_service = EmployeeService()
        result_list = []
        for entity in entity_list:
            employee_entity = employee_service.read_employee(employ_id=entity.employ_id)
            shift_time = datetime.strptime("%H:%M", employee_entity.shift_time)

            status = "late"
            if shift_time > entity.enter_time.time():
                status = "on-time"

            result_list.append(
                QueryEnterRecord(
                    employee_id=employee_entity.employ_id,
                    zone=employee_entity.zone,
                    shift_time=employee_entity.shift_time,
                    status=status,
                )
            )
