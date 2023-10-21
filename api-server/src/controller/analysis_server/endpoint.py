from typing import Annotated

from fastapi import APIRouter, Path

from src.controller.analysis_server.schema.post_chat_msg import (
    PostChatMsgRequestBody,
    PostChatMsgResponseBody,
)
from src.controller.analysis_server.schema.post_report_msg import (
    PostReportMsgRequestBody,
    PostReportMsgResponseBody,
)
from src.service.analysis_server_service import AnalysisServerService

analysis_server_router = APIRouter(
    prefix="/AnalysisServer",
    tags=["Analysis Server"]
)

service = AnalysisServerService()

@analysis_server_router.post(
    "/chat",
    response_model = PostChatMsgResponseBody,
)
def chat(body: PostChatMsgRequestBody):
    return service.chat_with_GPT(body)

@analysis_server_router.post(
    "/report",
    response_model = PostReportMsgResponseBody,
)
def chat(body: PostReportMsgRequestBody):
    return service.weekly_report_GPT(body)