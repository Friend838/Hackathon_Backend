import json
import os
import shutil
from typing import Annotated

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse

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
    print(type(results))
    results = {"results": json.dumps(results)}

    return FileResponse(processed_img_path, headers=results, media_type="image/jpg")
