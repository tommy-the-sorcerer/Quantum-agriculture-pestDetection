import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import cv2
import numpy as np
from app.services.pipeline import validate_specimen_quality, process_and_predict


def test_webcam_selfie_rejected():
    webcam_path = PROJECT_ROOT / "static" / "uploads" / "upload_1791605179670_camera-leaf-1791605178094.jpg"
    if not webcam_path.exists():
        return
    img = cv2.imread(str(webcam_path))
    is_valid, reason, msg = validate_specimen_quality(img)
    assert is_valid is False, f"Webcam selfie must be rejected, got: {reason}"
    print(f"[PASS] Webcam selfie rejected properly: reason={reason}")

    with open(webcam_path, "rb") as f:
        data = f.read()
    res = process_and_predict(data, crop_code="maize")
    assert res["valid"] is False, "process_and_predict must return valid=False for selfie"
    print(f"[PASS] process_and_predict rejected selfie with message: {res['message']}")

def test_genuine_leaf_accepted():
    leaf_path = PROJECT_ROOT / "datasets" / "golden_test" / "pigeonpea" / "leaf_spot" / "images (104).jpg"
    assert leaf_path.exists(), "Leaf image must exist"
    img = cv2.imread(str(leaf_path))
    is_valid, reason, msg = validate_specimen_quality(img)
    assert is_valid is True, f"Genuine leaf must pass validation, got: {reason}"

    with open(leaf_path, "rb") as f:
        data = f.read()
    res = process_and_predict(data, crop_code="pigeonpea")
    assert res["valid"] is True, "process_and_predict must return valid=True for genuine leaf"
    print(f"[PASS] Genuine leaf accepted: condition={res.get('condition')}, confidence={res.get('confidence')}")

if __name__ == "__main__":
    test_webcam_selfie_rejected()
    test_genuine_leaf_accepted()
    print("All validation tests passed successfully!")
