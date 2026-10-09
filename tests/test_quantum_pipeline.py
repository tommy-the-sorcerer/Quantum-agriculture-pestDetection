"""
Automated Integration Test for FALCON-Q (IBM Qiskit Multimodal Pipeline)
Tests:
1. Feature vector extraction and scaling to [0, pi]
2. Qiskit circuit execution and statevector evolution
3. FastAPI endpoint /api/quantum/early-warning with live/mock payload
"""

import sys
from pathlib import Path
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.services.multimodal_encoder import encode_multimodal_quantum_vector
from app.services.quantum_engine import quantum_engine
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_multimodal_encoding():
    weather = {"temperature": 27.5, "humidity": 88.0, "rainfall": 2.0, "available": True}
    fake_img = np.zeros((200, 200, 3), dtype=np.uint8)
    fake_img[:, :, 1] = 180  # green leaf simulation

    vec = encode_multimodal_quantum_vector(fake_img, weather, "vegetative")
    assert len(vec) == 4, "Vector must be 4-dimensional"
    assert np.all(vec >= 0.0) and np.all(vec <= np.pi + 1e-5), "Features must be within [0, pi]"
    print("[PASS] Multimodal encoding test: 4D vector correctly bounded in [0, pi]")

def test_quantum_engine_inference():
    test_vec = np.array([0.5 * np.pi, 0.7 * np.pi, 0.8 * np.pi, 0.9 * np.pi])
    res = quantum_engine.predict_early_warning(test_vec, {"temperature": 28.0, "humidity": 90.0, "rainfall": 0.0, "wind_speed": 5.0})

    assert res["success"] is True
    assert 0.0 <= res["outbreak_probability"] <= 1.0
    assert res["circuit_specs"]["num_qubits"] == 4
    assert res["circuit_specs"]["hilbert_space_dimension"] == 16
    assert len(res["qubit_telemetry"]) == 4
    print(f"[PASS] Quantum Engine execution: Probability={res['outbreak_percentage']}%, Risk={res['risk_level']}, LeadTime={res['prediction_lead_time_hours']}h")

def test_api_endpoint():
    resp = client.post("/api/quantum/early-warning", data={
        "district": "Nashik",
        "crop": "pigeonpea",
        "growth_stage": "flowering"
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert "quantum_framework" in data
    assert "circuit_specs" in data
    assert data["circuit_specs"]["num_qubits"] == 4
    print("[PASS] FastAPI /api/quantum/early-warning endpoint returned 200 OK with valid Qiskit response!")

def test_api_endpoint_with_image():
    sample_img_path = PROJECT_ROOT / "datasets" / "golden_test" / "pigeonpea" / "leaf_spot" / "images (104).jpg"
    assert sample_img_path.exists(), "Sample test image must exist"
    
    with open(sample_img_path, "rb") as f:
        img_bytes = f.read()

    # 1. Test dedicated quantum endpoint with file upload
    resp_q = client.post(
        "/api/quantum/early-warning",
        data={"district": "Nashik", "crop": "pigeonpea", "growth_stage": "flowering"},
        files={"file": ("leaf_spot.jpg", img_bytes, "image/jpeg")}
    )
    assert resp_q.status_code == 200
    data_q = resp_q.json()
    assert data_q["success"] is True
    assert data_q["circuit_specs"]["num_qubits"] == 4
    print(f"[PASS] /api/quantum/early-warning with real leaf image: Risk={data_q['risk_level']}, Prob={data_q['outbreak_percentage']}%")

    # 2. Test main diagnosis /predict pipeline with quantum integration
    resp_p = client.post(
        "/predict",
        data={"crop": "pigeonpea", "growth_stage": "flowering", "district": "Nashik"},
        files={"file": ("leaf_spot.jpg", img_bytes, "image/jpeg")}
    )
    assert resp_p.status_code == 200
    data_p = resp_p.json()
    assert data_p.get("valid") is True
    assert "quantum_early_warning" in data_p
    assert data_p["quantum_early_warning"] is not None
    assert data_p["quantum_early_warning"]["circuit_specs"]["num_qubits"] == 4
    print(f"[PASS] /predict pipeline with quantum early warning integration verified: Q-LeadTime={data_p['quantum_early_warning']['prediction_lead_time_hours']}h")

def test_circuit_details_endpoint():
    resp = client.get("/api/quantum/circuit")
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["num_qubits"] == 4
    assert data["hilbert_space_dimension"] == 16
    assert "operations_count" in data
    assert "ascii_diagram" in data
    assert "diagram_url" in data
    print(f"[PASS] /api/quantum/circuit returned full gate decomposition! Operations: {data['operations_count']}")

if __name__ == "__main__":
    test_multimodal_encoding()
    test_quantum_engine_inference()
    test_api_endpoint()
    test_api_endpoint_with_image()
    test_circuit_details_endpoint()
    print("\nALL QUANTUM INTEGRATION TESTS PASSED (100% SUCCESS)!")


