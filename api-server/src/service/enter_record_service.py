# pylint: disable=import-error
from src.controller.enter_record.schema.post_enter_record import (
    PostEnterRecordRequestBody,
    PostEnterRecordResponseBody,
)
from src.entity.enter_record_entity import EnterRecord
from src.infra.repo.enter_record_repo import EnterRecordRepo


class EnterRecordService:
    def __init__(self) -> None:
        self.repo = EnterRecordRepo()

    def process_enter_record(self, body: PostEnterRecordRequestBody):
        enter_record_entity = EnterRecord(body.model_dump())

        # model inference
        # return labeled_img, target, confidence, position, danger

        enter_record_entity.labeled_img = "TBA"
        enter_record_entity.target = "TBA"
        enter_record_entity.confidence = "TBA"
        enter_record_entity.position = "TBA"
        enter_record_entity.danger = "TBA"

        return PostEnterRecordResponseBody(
            **self.repo.post_enter_record(enter_record_entity)
        )
