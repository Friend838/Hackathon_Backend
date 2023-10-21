# pylint: disable=import-error
from src.entity.weekly_report_entity import WeeklyReport
from src.infra.database.mongo_db import MongoDB


class WeeklyReportRepo:
    def __init__(self) -> None:
        self.db = MongoDB()
        self.collection_name = "WeeklyReport"

    def post_weekly_report(self, weekly_report_entity: WeeklyReport):
        object_id = self.db.insert_one_doc(
            self.collection_name, weekly_report_entity.to_dict()
        )
        return {"mongo_object_id": object_id}
