import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_voice_command_english_maize_gallery():
    payload = {
        "text": "I have an IMAGE of a plant in my gallery and i need to upload the image take to me the image upload panel and select the maize crop and then click on the choose from gallery option",
        "lang": "en-IN"
    }
    resp = client.post("/api/voice-command", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["crop"] == "maize"
    assert data["action"] == "open_gallery"
    assert data["target_view"] == "diagnose"
    assert "maize" in data["reply_text"].lower() or "gallery" in data["reply_text"].lower()

def test_voice_command_telugu_maize_gallery():
    payload = {
        "text": "మొక్కజొన్న పంట ఎంచుకుని గ్యాలరీ ఫోటో ఓపెన్ చేయండి",
        "lang": "te-IN"
    }
    resp = client.post("/api/voice-command", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["crop"] == "maize"
    assert data["action"] == "open_gallery"
    assert data["target_view"] == "diagnose"
    assert len(data["reply_text"]) > 0

def test_voice_command_casual_chat():
    payload = {
        "text": "Hi ela unnav",
        "lang": "te-IN"
    }
    resp = client.post("/api/voice-command", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["intent"] == "general_chat"
    assert data["action"] == "none"
    assert len(data["reply_text"]) > 0

def test_voice_command_change_language_hindi():
    payload = {
        "text": "change website language to hindi",
        "lang": "en-IN"
    }
    resp = client.post("/api/voice-command", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["intent"] == "change_language"
    assert data["target_language"] == "hi"
    assert "हिंदी" in data["reply_text"] or "hindi" in data["reply_text"].lower()

def test_voice_command_change_language_marathi():
    payload = {
        "text": "वेबसाइटची भाषा मराठी करा",
        "lang": "mr-IN"
    }
    resp = client.post("/api/voice-command", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["intent"] == "change_language"
    assert data["target_language"] == "mr"
    assert "मराठी" in data["reply_text"]
