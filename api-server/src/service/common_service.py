# pylint: disable=import-error
from src.dependencies.yolov7.class_detect import tsmc_model


class Common:
    def __init__(self) -> None:
        self.model_predictor = tsmc_model()

    def model_inference(self, image_path: str) -> str:
        results = self.model_predictor.detect(image_path)
        print(results)

        img_name = image_path.split("/")[-1]
        processed_img_path = f"../images/labeled/{img_name}"
        if not results:
            processed_img_path = f"../images/origin/{img_name}"

        return processed_img_path, results
