# pylint: disable=import-error
from src.entity.machine_record_entity import MachineRecord
from src.infra.database.mongo_db import MongoDB


class MachineRecordRepo:
    def __init__(self) -> None:
        self.db = MongoDB()
        self.collection_name = "MachineRecord"

    def post_machine_record(self, machine_record_entity: MachineRecord):
        payload = machine_record_entity.to_dict()
        object_id = self.db.insert_one_doc(self.collection_name, payload)
        return {"mongo_object_id": object_id}
