import json
import os
import shutil
from typing import Annotated

from camel_converter import dict_to_camel
from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import FileResponse
from src.controller.common.schema.post_generate_record import PostGenerateRecord

# pylint: disable=import-error
from src.service.common_service import Common

service = Common()
common_router = APIRouter(prefix="/common", tags=["common"])


@common_router.post(path="/imageInference", response_class=FileResponse)
def inference_image(
    img_file: Annotated[UploadFile, File()],
):
    print(img_file.filename)
    file_path = f"../images/origin/{img_file.filename}"

    if not os.path.isdir("../images/origin/"):
        os.mkdir("../images/origin/")
    if not os.path.isdir("../images/labeled/"):
        os.mkdir("../images/labeled/")

    with open(file_path, "wb+") as file_object:
        shutil.copyfileobj(img_file.file, file_object)

    processed_img_path, results = service.model_inference(file_path)
    results = {"results": json.dumps(dict_to_camel(results))}

    return FileResponse(processed_img_path, headers=results, media_type="image/jpg")


@common_router.post(
    path="/generateRecord",
    response_model=PostGenerateRecord,
)
def generate_record(
    img_file: Annotated[UploadFile, File()],
    employee_id: Annotated[str, Form()],
    zone: Annotated[str, Form()],
    enter_time: Annotated[int, Form()],
    tool_scan_time: Annotated[float, Form()],
):
    file_path = f"../images/origin/{img_file.filename}"

    if not os.path.isdir("../images/origin/"):
        os.mkdir("../images/origin/")
    if not os.path.isdir("../images/labeled/"):
        os.mkdir("../images/labeled/")

    with open(file_path, "wb+") as file_object:
        shutil.copyfileobj(img_file.file, file_object)

    service.generate_record(
        image_path=file_path,
        employee_id=employee_id,
        zone=zone,
        enter_time=enter_time,
        tool_scan_time=tool_scan_time,
    )

    return {"status": "success"}
