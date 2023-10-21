# pylint: disable=import-error
from src.entity.enter_record_entity import EnterRecord
from src.infra.database.mongo_db import MongoDB


class EnterRecordRepo:
    def __init__(self) -> None:
        self.db = MongoDB()
        self.collection_name = "EnterRecord"

    def post_enter_record(self, enter_record_entity: EnterRecord):
        payload = enter_record_entity.to_dict()
        object_id = self.db.insert_one_doc(self.collection_name, payload)
        return {"mongo_object_id": object_id}

    def get_enter_record(
        self, start_timestamp: int, end_timestamp: int
    ) -> list[EnterRecord]:
        query_result = self.db.find(
            self.collection_name,
            {"enter_time": {"$gte": start_timestamp, "$lte": end_timestamp}},
        )

        return [EnterRecord(item) for item in query_result]
