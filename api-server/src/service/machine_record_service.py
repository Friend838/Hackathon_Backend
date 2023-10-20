# pylint: disable=import-error
from src.controller.machine_record.schema.post_machine_record import (
    PostMachineRecordRequestBody,
    PostMachineRecordResponseBody,
)
from src.entity.machine_record_entity import MachineRecord
from src.infra.repo.machine_record_repo import MachineRecordRepo


class MachineRecordService:
    def __init__(self) -> None:
        self.repo = MachineRecordRepo()

    def post_machine_record(
        self, body: PostMachineRecordRequestBody
    ) -> PostMachineRecordResponseBody:
        return PostMachineRecordResponseBody(
            **self.repo.post_machine_record(MachineRecord(body.model_dump()))
        )
