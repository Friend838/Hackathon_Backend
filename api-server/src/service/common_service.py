# pylint: disable=import-error
from src.controller.enter_record.schema.post_enter_record import (
    PostEnterRecordRequestBody,
)
from src.controller.machine_record.schema.post_machine_record import (
    PostMachineRecordRequestBody,
)
from src.dependencies.yolov7.class_detect import tsmc_model
from src.service.enter_record_service import EnterRecordService
from src.service.machine_record_service import MachineRecordService


class Common:
    def __init__(self) -> None:
        self.model_predictor = tsmc_model()
        self.enter_record_service = EnterRecordService()
        self.machine_record_service = MachineRecordService()

    def model_inference(self, image_path: str) -> str:
        results = self.model_predictor.detect(image_path)
        print(results)

        class_label = [item["class"] for item in results]
        status = None
        if 2 in class_label or 3 in class_label or 4 in class_label:
            status = 2
        elif 0 in class_label or 1 in class_label:
            status = 1
        else:
            status = 0

        img_name = image_path.split("/")[-1]
        processed_img_path = f"../images/labeled/{img_name}"
        if not results:
            processed_img_path = f"../images/origin/{img_name}"

        return processed_img_path, {"inference_result": results, "status": status}

    def generate_record(
        self,
        image_path: str,
        employee_id: str,
        zone: str,
        enter_time: int,
        tool_scan_time: float,
    ) -> str:
        results = self.model_predictor.detect(image_path)
        print(results)

        class_label = [item["class"] for item in results]
        status = None
        if 2 in class_label or 3 in class_label or 4 in class_label:
            status = 2
        elif 0 in class_label or 1 in class_label:
            status = 1
        else:
            status = 0

        img_name = image_path.split("/")[-1]
        origin_img_path = f"../images/origin/{img_name}"
        processed_img_path = f"../images/labeled/{img_name}"
        if not results:
            processed_img_path = f"../images/origin/{img_name}"

        self.enter_record_service.process_enter_record(
            PostEnterRecordRequestBody(
                employee_id=employee_id,
                enter_time=enter_time,
                origin_img=origin_img_path,
                labeled_img=processed_img_path,
                target=[item["class"] for item in results],
                confidence=[item["confidence"] for item in results],
                position=[item["xywh"] for item in results],
                danger=status,
            )
        )

        self.machine_record_service.post_machine_record(
            PostMachineRecordRequestBody(
                zone=zone,
                tool_scan_time=tool_scan_time,
                timestamp=enter_time,
            )
        )
