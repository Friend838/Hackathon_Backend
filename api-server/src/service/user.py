from datetime import datetime

from dateutil import tz

# pylint: disable=import-error
from src.controller.user.schema.post_user import (
    PostUserRequestBody,
    PostUserResponseBody,
)
from src.controller.user.schema.query_user import QueryUser
from src.infra.repo.mongo_user import MongoUserRepo


class UserService:
    def __init__(self) -> None:
        self.repo = MongoUserRepo()

    def read_user(self, user_id: str):
        user_entity = self.repo.read_user(user_id)
        return QueryUser(**user_entity.to_dict())

    def create_user(self, body: PostUserRequestBody):
        item = {
            "id": body.id,
            "name": body.name,
            "age": body.age,
            "birthday": body.birthday,
        }
        return PostUserResponseBody(**self.repo.create_user(item))
