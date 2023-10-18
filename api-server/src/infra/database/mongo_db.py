from typing import Any

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.results import DeleteResult

# pylint: disable=import-error
from src.dependencies.settings import get_settings


class MongoDB(object):
    def __new__(cls) -> Any:
        if not hasattr(cls, "instance") or not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        setting = get_settings()
        self.__client = MongoClient(
            f"mongodb://{setting.db_username}:{setting.db_password}@{setting.db_host}:{setting.db_port}/"
        )
        try:
            self.__client["admin"].command("ismaster")
        except ConnectionFailure:
            print("****************connected failed********************")

        self.db = self.__client[setting.database]

    def find(self, collection: str, document: dict) -> dict:
        return list(item for item in self.db[collection].find(document))

    def insert_one_doc(self, collection: str, document: dict) -> str:
        insert_result = self.db[collection].insert_one(document)
        if insert_result.inserted_id:
            return str(insert_result.inserted_id)
        else:
            return False

    def delete_one_doc(self, collection: str, document: dict) -> DeleteResult:
        return self.db[collection].delete_one(document)
