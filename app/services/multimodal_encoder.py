"""
Multimodal Agricultural Feature Encoder for FALCON-Q
Fuses foliar computer vision with Open-Meteo microclimate telemetry.
Outputs a normalized 4-dimensional vector scaled to [0, pi] for Qiskit quantum state encoding.
"""

import cv2
import numpy as np
from typing import Dict, Any, Tuple, Optional

# Fungal/pest germination temperature optimal range in Celsius (e.g. blights, mildews, rusts)
OPTIMAL_GERMINATION_TEMP_MIN = 18.0
OPTIMAL_GERMINATION_TEMP_MAX = 30.0

def extract_foliar_visual_features(img_bgr: np.ndarray) -> Tuple[float, float]:
    """
    Extracts continuous foliar health features from RGB leaf specimen:
    1. Chlorophyll Green Pigment Ratio (f0): Proportion of active chlorophyll foliage.
    2. Subtle Foliar Variance / Early Stress Index (f1): High frequency texture & necrotic discoloration.
    """
    if img_bgr is None or img_bgr.size == 0:
        return 0.5, 0.5

    h, w = img_bgr.shape[:2]
    total_pixels = max(h * w, 1)

    # Convert to HSV color space for vegetative pigment analysis
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

    # Healthy Chlorophyll Green mask: Hue 35 to 85, Saturation >= 40, Value >= 40
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    green_ratio = float(np.count_nonzero(green_mask)) / float(total_pixels)

    # Necrotic / Chlorotic Yellow-Brown mask: Hue 10 to 35, Saturation >= 50
    lower_necrotic = np.array([10, 50, 40])
    upper_necrotic = np.array([35, 255, 255])
    necrotic_mask = cv2.inRange(hsv, lower_necrotic, upper_necrotic)
    necrotic_ratio = float(np.count_nonzero(necrotic_mask)) / float(total_pixels)

    # Compute cellular surface texture variance using Laplacian filter
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    laplacian_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    normalized_texture = float(np.clip(laplacian_var / 500.0, 0.0, 1.0))

    # Feature 0: Foliar Health Score (higher means healthier green foliage)
    foliar_health = float(np.clip(green_ratio * 1.5 - necrotic_ratio * 2.0, 0.0, 1.0))

    # Feature 1: Early Stress Factor (combination of necrosis and irregular texture)
    early_stress = float(np.clip(necrotic_ratio * 3.0 + normalized_texture * 0.4, 0.0, 1.0))

    return foliar_health, early_stress


def extract_microclimate_features(weather: Optional[Dict[str, Any]]) -> Tuple[float, float]:
    """
    Computes microclimate favorability scores for spore germination:
    1. Thermal Germination Score (f2): Proximity of temperature to optimal fungal proliferation band.
    2. Moisture Hazard Score (f3): Atmospheric relative humidity and rain probability.
    """
    if not weather or not weather.get("available", False):
        # Default nominal field conditions: 26°C, 65% humidity
        temp = 26.0
        humidity = 65.0
        rain = 0.0
    else:
        temp = float(weather.get("temperature") or 26.0)
        humidity = float(weather.get("humidity") or 65.0)
        rain = float(weather.get("rainfall") or 0.0)

    # Thermal score: Maximum (1.0) when temperature is in the 22-26°C fungal sweet spot
    if OPTIMAL_GERMINATION_TEMP_MIN <= temp <= OPTIMAL_GERMINATION_TEMP_MAX:
        # Distance from optimal center (24°C)
        thermal_score = 1.0 - (abs(temp - 24.0) / 12.0)
    elif temp < OPTIMAL_GERMINATION_TEMP_MIN:
        thermal_score = max(0.0, 1.0 - (OPTIMAL_GERMINATION_TEMP_MIN - temp) / 10.0)
    else:
        thermal_score = max(0.0, 1.0 - (temp - OPTIMAL_GERMINATION_TEMP_MAX) / 10.0)
    thermal_score = float(np.clip(thermal_score, 0.0, 1.0))

    # Moisture hazard: Relative humidity > 70% drastically accelerates fungal sporulation
    humidity_factor = float(np.clip((humidity - 40.0) / 50.0, 0.0, 1.0))
    rain_factor = 0.3 if rain > 0.0 else 0.0
    moisture_score = float(np.clip(humidity_factor + rain_factor, 0.0, 1.0))

    return thermal_score, moisture_score


def encode_multimodal_quantum_vector(
    img_bgr: Optional[np.ndarray],
    weather: Optional[Dict[str, Any]],
    crop_stage: str = "vegetative"
) -> np.ndarray:
    """
    Fuses foliar vision with micro-climate into a 4-dimensional vector scaled strictly to [0, pi]
    for Qiskit ZZFeatureMap gate angle parameterization.

    Vector Components:
    x[0]: Foliar Pigment & Cellular Health (scaled 0 to pi)
    x[1]: Early Stress Discoloration Index (scaled 0 to pi)
    x[2]: Thermal Spore Proliferation Risk (scaled 0 to pi)
    x[3]: Microclimate Moisture & Humidity Hazard (scaled 0 to pi)
    """
    f0, f1 = extract_foliar_visual_features(img_bgr) if img_bgr is not None else (0.5, 0.5)
    f2, f3 = extract_microclimate_features(weather)

    # Adjust stress if in flowering/fruiting stage
    stage_key = (crop_stage or "").lower()
    if stage_key in ("flowering", "fruiting", "fruiting_pod"):
        f1 = min(1.0, f1 * 1.15)
        f3 = min(1.0, f3 * 1.10)

    raw_features = np.array([f0, f1, f2, f3], dtype=np.float64)

    # Scale continuous [0.0, 1.0] domain to [0.0, pi] for quantum rotational gates
    quantum_vector = raw_features * np.pi
    return quantum_vector
