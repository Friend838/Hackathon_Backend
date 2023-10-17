from typing import Annotated

from fastapi import APIRouter, Path, Query
from src.controller.user.schema.post_user import (
    PostUserRequestBody,
    PostUserResponseBody,
)
from src.controller.user.schema.query_user import QueryUser
from src.service.user import UserService

user_router = APIRouter(
    tags=["test"],
    responses={404: {"description": "Not found"}},
)

service = UserService()


@user_router.get(
    "/user/{user_id}",
    response_model=QueryUser,
)
def read_user(user_id: Annotated[str, Path(title="The ID of user to get")]):
    return service.read_user(user_id)


@user_router.post(
    "/user",
    response_model=PostUserResponseBody,
)
def create_user(body: PostUserRequestBody):
    return service.create_user(body)
