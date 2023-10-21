import argparse
import time
from pathlib import Path

import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random

# pylint: disable=import-error
from .models.experimental import attempt_load
from .utils.datasets import LoadImages, LoadStreams
from .utils.general import (
    apply_classifier,
    check_img_size,
    check_imshow,
    check_requirements,
    increment_path,
    non_max_suppression,
    scale_coords,
    set_logging,
    strip_optimizer,
    xyxy2xywh,
)
from .utils.plots import plot_one_box
from .utils.torch_utils import (
    TracedModel,
    load_classifier,
    select_device,
    time_synchronized,
)


class tsmc_model:
    def __init__(self) -> None:
        # Arguments
        self.weights = "./src/dependencies/yolov7/models/best.pt"
        self.imgsz = 1280
        self.conf_thres = 0.25
        self.iou_thres = 0.45
        self.device = "cpu"
        self.view_img = False
        self.save_txt = False
        self.save_conf = True
        self.nosave = False
        self.classes = None
        self.agnostic_nms = False
        self.augment = False
        self.update = False
        self.project = "../images/labeled"
        self.name = "exp"
        self.exist_ok = False
        self.no_trace = True
        self.trace = False

        # Model
        # Initialize
        set_logging()
        self.device = select_device(self.device)
        self.half = self.device.type != "cpu"  # half precision only supported on CUDA

        # Load model
        self.model = attempt_load(
            self.weights, map_location=self.device
        )  # load FP32 model
        self.stride = int(self.model.stride.max())  # model stride
        imgsz = check_img_size(self.imgsz, s=self.stride)  # check img_size

        if self.trace:
            self.model = TracedModel(self.model, self.device, self.imgsz)

        if self.half:
            self.model.half()  # to FP16

        # Second-stage classifier
        self.classify = False
        if self.classify:
            self.modelc = load_classifier(name="resnet101", n=2)  # initialize
            self.modelc.load_state_dict(
                torch.load("weights/resnet101.pt", map_location=self.device)["model"]
            ).to(self.device).eval()

        return

    def detect(self, source: str, ave_img=False):
        # source, weights, view_img, save_txt, imgsz, trace = self.source, self.weights, self.view_img, self.save_txt, self.img_size, not self.no_trace
        res = []
        save_img = not self.nosave and not source.endswith(
            ".txt"
        )  # save inference images
        webcam = (
            source.isnumeric()
            or source.endswith(".txt")
            or source.lower().startswith(("rtsp://", "rtmp://", "http://", "https://"))
        )

        # Directories
        save_dir = Path("../images/labeled")
        # save_dir = Path(
        #     increment_path(Path(self.project), exist_ok=self.exist_ok)
        # )  # increment run
        # (save_dir / "labels" if self.save_txt else save_dir).mkdir(
        #     parents=True, exist_ok=True
        # )  # make dir

        # Set Dataloader
        vid_path, vid_writer = None, None
        if webcam:
            self.view_img = check_imshow()
            cudnn.benchmark = True  # set True to speed up constant image size inference
            dataset = LoadStreams(source, img_size=self.imgsz, stride=self.stride)
        else:
            dataset = LoadImages(source, img_size=self.imgsz, stride=self.stride)

        # Get names and colors
        names = (
            self.model.module.names
            if hasattr(self.model, "module")
            else self.model.names
        )
        colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

        # Run inference
        if self.device.type != "cpu":
            self.model(
                torch.zeros(1, 3, self.imgsz, self.imgsz)
                .to(self.device)
                .type_as(next(self.model.parameters()))
            )  # run once
        old_img_w = old_img_h = self.imgsz
        old_img_b = 1

        t0 = time.time()
        for path, img, im0s, vid_cap in dataset:
            img = torch.from_numpy(img).to(self.device)
            img = img.half() if self.half else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)

            # Warmup
            if self.device.type != "cpu" and (
                old_img_b != img.shape[0]
                or old_img_h != img.shape[2]
                or old_img_w != img.shape[3]
            ):
                old_img_b = img.shape[0]
                old_img_h = img.shape[2]
                old_img_w = img.shape[3]
                for i in range(3):
                    self.model(img, augment=self.augment)[0]

            # Inference
            t1 = time_synchronized()
            with torch.no_grad():  # Calculating gradients would cause a GPU memory leak
                pred = self.model(img, augment=self.augment)[0]
            t2 = time_synchronized()

            # Apply NMS
            pred = non_max_suppression(
                pred,
                self.conf_thres,
                self.iou_thres,
                classes=self.classes,
                agnostic=self.agnostic_nms,
            )
            t3 = time_synchronized()

            # Apply Classifier
            if self.classify:
                pred = apply_classifier(pred, self.modelc, img, im0s)

            # Process detections
            for i, det in enumerate(pred):  # detections per image
                if webcam:  # batch_size >= 1
                    p, s, im0, frame = (
                        path[i],
                        "%g: " % i,
                        im0s[i].copy(),
                        dataset.count,
                    )
                else:
                    p, s, im0, frame = path, "", im0s, getattr(dataset, "frame", 0)

                p = Path(p)  # to Path
                save_path = str(save_dir / p.name)  # img.jpg
                txt_path = str(save_dir / "labels" / p.stem) + (
                    "" if dataset.mode == "image" else f"_{frame}"
                )  # img.txt
                gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                if len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_coords(
                        img.shape[2:], det[:, :4], im0.shape
                    ).round()

                    # Print results
                    for c in det[:, -1].unique():
                        n = (det[:, -1] == c).sum()  # detections per class
                        s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                    # Write results
                    for *xyxy, conf, cls in reversed(det):
                        if self.save_txt:  # Write to file
                            xywh = (
                                (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn)
                                .view(-1)
                                .tolist()
                            )  # normalized xywh
                            line = (
                                (cls, *xywh, conf) if self.save_conf else (cls, *xywh)
                            )  # label format
                            with open(txt_path + ".txt", "a") as f:
                                f.write(("%g " * len(line)).rstrip() % line + "\n")

                        if save_img or self.view_img:  # Add bbox to image
                            label = f"{names[int(cls)]} {conf:.2f}"
                            plot_one_box(
                                xyxy,
                                im0,
                                label=label,
                                color=colors[int(cls)],
                                line_thickness=1,
                            )

                    for *xyxy, conf, cls in reversed(det):
                        xywh = (
                            (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn)
                            .view(-1)
                            .tolist()
                        )  # normalized xywh
                        line = (
                            (cls, *xywh, conf) if self.save_conf else (cls, *xywh)
                        )  # label format
                        res.append(
                            {
                                "class": int(cls.item()),
                                "xywh": xywh,
                                "confidence": conf.item(),
                            }
                        )

                # Print time (inference + NMS)
                print(
                    f"{s}Done. ({(1E3 * (t2 - t1)):.1f}ms) Inference, ({(1E3 * (t3 - t2)):.1f}ms) NMS"
                )

                # Stream results
                # if self.view_img:
                #     cv2.imshow(str(p), im0)
                #     cv2.waitKey(1)  # 1 millisecond

                # Save results (image with detections)
                if save_img:
                    if dataset.mode == "image":
                        print(save_path)
                        cv2.imwrite(save_path, im0)
                        print(f" The image with the result is saved in: {save_path}")
                #     else:  # 'video' or 'stream'
                #         if vid_path != save_path:  # new video
                #             vid_path = save_path
                #             if isinstance(vid_writer, cv2.VideoWriter):
                #                 vid_writer.release()  # release previous video writer
                #             if vid_cap:  # video
                #                 fps = vid_cap.get(cv2.CAP_PROP_FPS)
                #                 w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                #                 h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                #             else:  # stream
                #                 fps, w, h = 30, im0.shape[1], im0.shape[0]
                #                 save_path += '.mp4'
                #             vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
                #         vid_writer.write(im0)

        # if self.save_txt or save_img:
        #     s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if self.save_txt else ''
        # print(f"Results saved to {save_dir}{s}")

        print(f"Done. ({time.time() - t0:.3f}s)")
        return res


if __name__ == "__main__":
    TSMC_model = tsmc_model()
    result = TSMC_model.detect()
    result = TSMC_model.detect()
    result = TSMC_model.detect()
    print(result)
