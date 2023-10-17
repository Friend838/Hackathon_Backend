from src.entity.user import User
from src.infra.database.mongo_db import MongoDB


class MongoUserRepo:
    def __init__(self) -> None:
        self.db = MongoDB()
        self.collection_name = "user"

    def read_user(self, user_id: str):
        document = {"id": user_id}
        result = self.db.find(self.collection_name, document)

        return User(result[0])

    def create_user(self, doc: dict):
        object_id = self.db.insert_one_doc(self.collection_name, User(doc).to_dict())
        return {"mongo_object_id": object_id}
