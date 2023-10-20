# pylint: disable=import-error
from src.infra.database.mongo_db import MongoDB
from src.entity.enter_record import EnterRecord


class EnterRecordRepo:
    def __init__(self) -> None:
        self.db = MongoDB()
    
    def post_enter_record(self, data: ):
        