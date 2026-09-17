from dataclasses import dataclass
from pathlib import Path
from typing import Any
import numpy as np

try:
    from PIL import Image
except Exception:
    Image = None


@dataclass
class DetectionResult:
    species: str
    confidence: float
    zone: str
    direction: str
    threat_state: str


class AnimalDetector:
    """Optional YOLO integration with a deterministic demo fallback."""

    def __init__(self, model_path: str = ""):
        self.model = None
        self.model_path = model_path
        if model_path and Path(model_path).exists():
            try:
                from ultralytics import YOLO
                self.model = YOLO(model_path)
            except Exception:
                self.model = None

    def infer_image(self, image_bytes: bytes) -> list[DetectionResult]:
        if not self.model or Image is None:
            return [DetectionResult("demo_animal", 0.91, "North-West", "South-East", "Approaching Crop")]
        from io import BytesIO
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        frame = np.array(image)
        results = self.model.track(frame, persist=True, verbose=False)
        detections: list[DetectionResult] = []
        for result in results:
            boxes = getattr(result, "boxes", None)
            if boxes is None:
                continue
            names = result.names
            for i in range(len(boxes)):
                cls_id = int(boxes.cls[i].item())
                conf = float(boxes.conf[i].item())
                label = names.get(cls_id, str(cls_id)) if isinstance(names, dict) else str(cls_id)
                detections.append(
                    DetectionResult(label, conf, "North-West", "South-East", "Approaching Crop")
                )
        return detections
