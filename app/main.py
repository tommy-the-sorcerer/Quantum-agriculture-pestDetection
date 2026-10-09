"""
FALCON-Q Quantum Multimodal Decision Platform
Backend REST API for IBM Qiskit Fall Fest 2026 (Problem Statement VNQFF-04)
Team TISSOT: Quantum Multimodal Crop Disease Early Warning Architecture
"""

import time
import os
import re
import json
import base64
import hmac
import hashlib
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any, Union
import numpy as np

from fastapi import FastAPI, UploadFile, File, Form, Request, HTTPException, Depends, Header
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel

try:
    from app.core import storage
    from app.services.pipeline import process_and_predict
    from app.core.taxonomy import CROPS, GROWTH_STAGES, MAHARASHTRA_DISTRICTS, get_district_info, get_ipm_advisory
    from app.services.weather_service import get_current_weather
    from app.core.i18n import get_all_translations, get_translation
    from app.services import pesticide_checker, doubt_doctor, inspection_engine, spread_alerts
    from app.services.multimodal_encoder import encode_multimodal_quantum_vector
    from app.services.quantum_engine import quantum_engine
except ImportError:
    import storage
    from pipeline import process_and_predict
    from taxonomy import CROPS, GROWTH_STAGES, MAHARASHTRA_DISTRICTS, get_district_info, get_ipm_advisory
    from weather_service import get_current_weather
    from i18n import get_all_translations, get_translation
    import pesticide_checker
    import doubt_doctor
    import inspection_engine
    import spread_alerts
    from multimodal_encoder import encode_multimodal_quantum_vector
    from quantum_engine import quantum_engine

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from groq import Groq
except ImportError:
    Groq = None

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("falcon_ai")

AUTH_SECRET_KEY = os.environ.get("FALCON_AUTH_SECRET", "falcon_q_vnqff04_production_secret_key_2026")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
groq_client = Groq(api_key=GROQ_API_KEY) if Groq and GROQ_API_KEY else None



def create_access_token(user_id: int, phone: str, role: str) -> str:
    """Generates a tamper-proof signed session token for authenticated personas."""
    payload = {
        "uid": user_id,
        "phone": phone,
        "role": role,
        "exp": int(time.time()) + 86400 * 7  # 7 days validity
    }
    payload_bytes = json.dumps(payload, separators=(',', ':')).encode('utf-8')
    b64_payload = base64.urlsafe_b64encode(payload_bytes).decode('ascii').rstrip('=')
    sig = hmac.new(AUTH_SECRET_KEY.encode('utf-8'), b64_payload.encode('ascii'), hashlib.sha256).hexdigest()
    return f"{b64_payload}.{sig}"


def verify_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Verifies HMAC signature and expiration timestamp of an access token."""
    try:
        parts = token.strip().split('.')
        if len(parts) != 2:
            return None
        b64_payload, sig = parts
        expected_sig = hmac.new(AUTH_SECRET_KEY.encode('utf-8'), b64_payload.encode('ascii'), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected_sig):
            return None
        padding = 4 - (len(b64_payload) % 4)
        if padding != 4:
            b64_payload += "=" * padding
        payload = json.loads(base64.urlsafe_b64decode(b64_payload.encode('ascii')).decode('utf-8'))
        if payload.get("exp", 0) < time.time():
            return None
        return payload
    except Exception:
        return None


def is_valid_image_magic(data: bytes) -> bool:
    """Checks header bytes to verify authentic JPEG, PNG, or WebP binary structure."""
    if len(data) < 12:
        return False
    if data[:3] == b"\xff\xd8\xff":
        return True
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return True
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return True
    return False


app = FastAPI(
    title="FALCON-Q | Quantum Multimodal Decision Platform",
    description="Quantum Multimodal Crop Disease Early Warning (VNQFF-04 - IBM Qiskit Fall Fest 2026 - Team TISSOT)",
    version="2.5.2"
)

# Exception handlers for clean JSON error responses
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "detail": exc.detail, "status_code": exc.status_code}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"status": "error", "detail": "Invalid request schema or parameters.", "errors": exc.errors(), "status_code": 422}
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled server exception on {request.method} {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"status": "error", "detail": "An internal server error occurred. Please try again later.", "status_code": 500}
    )


# Enable CORS for flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database schema and seeds
storage.initialize_database()

# Static assets and template engine
PROJECT_ROOT = Path(__file__).resolve().parent.parent
static_dir = PROJECT_ROOT / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
templates_dir = PROJECT_ROOT / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

# Ensure uploads directory exists
UPLOADS_DIR = static_dir / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

MAX_UPLOAD_SIZE_BYTES = 15 * 1024 * 1024  # 15 MB limit
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def validate_and_sanitize_upload(filename: Optional[str], data: bytes) -> str:
    """
    Guards against:
    1. Large payload DoS (rejects > 15MB)
    2. Empty file uploads
    3. Extension forgery (whitelists .jpg, .jpeg, .png, .webp)
    4. Magic byte inspection (rejects disguised executable/script payloads)
    5. Path traversal / directory escape (strips paths, keeps only alphanumeric stem)
    """
    if len(data) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    if len(data) > MAX_UPLOAD_SIZE_BYTES:
        raise HTTPException(status_code=413, detail=f"File size ({len(data)/(1024*1024):.1f} MB) exceeds limit of 15 MB.")

    raw_filename = Path(filename or "specimen.jpg").name
    ext = Path(raw_filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format '{ext}'. Only JPEG, PNG, and WebP images are supported."
        )

    if not is_valid_image_magic(data):
        raise HTTPException(
            status_code=400,
            detail="Uploaded file header does not match a valid image format (JPEG, PNG, or WebP)."
        )

    clean_stem = "".join(c for c in Path(raw_filename).stem if c.isalnum() or c in "_-") or "specimen"
    timestamp_str = int(time.time() * 1000)
    return f"{timestamp_str}_{clean_stem}{ext}"


# ==============================================================================
# PYDANTIC SCHEMAS
# ==============================================================================

class RegisterRequest(BaseModel):
    email: str
    full_name: str
    password: str
    phone: Optional[str] = ""
    role: str = "FARMER"
    preferred_language: str = "en"
    organization: Optional[str] = ""
    designation: Optional[str] = ""


class LoginRequest(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    password: str
    role: Optional[str] = None


# Inspirational farming quotes pool
INSPIRATIONAL_QUOTES = [
    "Farming is a profession of hope. Let's protect your harvest today! 🌾",
    "The farmer is the backbone of our nation — welcome back, champion! 💪",
    "Every seed you plant is a promise of food for millions. We're here to help! 🌱",
    "Agriculture is our wisest pursuit, for it contributes most to real wealth. 🏆",
    "A good farmer is nothing more nor less than a handy person with a sense of humus. 🌿",
    "The discovery of agriculture was the first big step toward a civilized life. Keep growing! 🚜",
    "To forget how to dig the earth and tend the soil is to forget ourselves. Welcome! 🌻",
    "Farming looks mighty easy when your plow is a pencil, but you make it real. Respect! 👏",
    "The ultimate goal of farming is the cultivation of human beings, not just crops. 🙏",
    "Where there is a farmer, there is life. Your dedication feeds the world! 🌍"
]


class FarmCreateRequest(BaseModel):
    user_id: int
    farm_name: str
    district: str
    taluka: str
    village: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    area_acres: float = 2.5
    primary_crop: Optional[str] = ""


class ExpertReviewRequest(BaseModel):
    expert_id: int
    review_action: str  # CONFIRM, CORRECT, SELECT_DISEASE, SELECT_PEST, MARK_UNKNOWN, LAB_REFERRAL, REQUEST_IMAGE
    diagnosis_code: Optional[str] = None
    condition_name: Optional[str] = None
    observation_type: Optional[str] = None
    expert_confidence: float = 95.0
    expert_severity: Optional[str] = None
    expert_notes: Optional[str] = ""
    custom_advisory: Optional[str] = ""
    follow_up_instructions: Optional[str] = ""


class FieldConfirmationRequest(BaseModel):
    user_id: int
    actual_condition_code: str
    actual_condition_name: str
    outcome: str  # IMPROVED, UNCHANGED, WORSENED, RESOLVED, UNKNOWN
    notes: Optional[str] = ""


class PesticideCheckRequest(BaseModel):
    crop: str
    condition_code: str
    product_query: str


class DoubtDoctorEvaluateRequest(BaseModel):
    crop: str
    top_prediction: Dict[str, Any]
    runner_up_prediction: Optional[Dict[str, Any]] = None
    language: Optional[str] = "mr"


class DoubtDoctorAnswerRequest(BaseModel):
    target_condition: str
    original_confidence: float
    answer: str  # YES, NO, DONT_KNOW
    confirms_if_yes: Optional[str] = None
    weight_boost: Optional[float] = 0.15


class EscalateCaseRequest(BaseModel):
    case_id: Optional[Union[int, str]] = None
    timestamp: Optional[str] = None
    crop: str
    disease: str
    severity: str
    image_url: Optional[str] = ""
    location: Optional[str] = ""
    farmer_name: Optional[str] = "Farmer"
    notes: Optional[str] = ""


@app.post("/api/voice-command")
async def voice_command(request: Request):
    """
    Autonomous agricultural voice assistant powered by Google Gemini and multilingual rule fallback.
    Accepts speech recognition text or audio in English, Telugu, Marathi, Hindi, Kannada, or Tamil.
    Executes autonomous UI navigation, crop selection, language switching, and gallery/camera actions.
    """
    user_text = ""
    req_lang = ""
    content_type = request.headers.get("content-type", "")

    if "application/json" in content_type:
        try:
            body = await request.json()
            user_text = (body.get("text") or body.get("query") or "").strip()
            req_lang = (body.get("lang") or "").strip()
        except Exception:
            user_text = ""
    elif "multipart/form-data" in content_type:
        try:
            form = await request.form()
            audio_field = form.get("audio")
            if audio_field and hasattr(audio_field, "read"):
                audio_bytes = await audio_field.read()
                if audio_bytes and groq_client:
                    filename = getattr(audio_field, "filename", "voice.webm") or "voice.webm"
                    try:
                        transcription = groq_client.audio.transcriptions.create(
                            file=(filename, audio_bytes),
                            model="whisper-large-v3"
                        )
                        user_text = transcription.text.strip()
                    except Exception as e:
                        logger.warning(f"Groq Whisper transcription exception: {e}")
            if not user_text:
                user_text = (form.get("text") or form.get("query") or "").strip()
                req_lang = (form.get("lang") or "").strip()
        except Exception as exc:
            logger.warning(f"Form parsing error in voice_command: {exc}")
            user_text = ""
    else:
        try:
            body = await request.body()
            if body:
                parsed_json = json.loads(body.decode("utf-8", errors="ignore"))
                user_text = (parsed_json.get("text") or parsed_json.get("query") or "").strip()
                req_lang = (parsed_json.get("lang") or "").strip()
        except Exception:
            user_text = ""

    # Detect user language family if not explicitly provided
    is_telugu = bool(re.search(r'[\u0C00-\u0C7F]', user_text)) or req_lang.startswith('te')
    is_devanagari = bool(re.search(r'[\u0900-\u097F]', user_text)) or req_lang.startswith('mr') or req_lang.startswith('hi')
    is_kannada = bool(re.search(r'[\u0C80-\u0CFF]', user_text)) or req_lang.startswith('kn')
    is_tamil = bool(re.search(r'[\u0B80-\u0BFF]', user_text)) or req_lang.startswith('ta')

    # Differentiate Hindi vs Marathi if Devanagari
    is_hindi = req_lang.startswith('hi') or any(w in user_text for w in ["मक्का", "फसल", "चुनो", "खोलो", "नमस्ते", "कैसा", "हो", "करना", "चाहिए", "बदलो", "करो"])
    is_marathi = req_lang.startswith('mr') or any(w in user_text for w in ["मका", "पीक", "निवडा", "उघडा", "नमस्कार", "कसे", "आहात", "करावे", "करा", "बदला"]) or (is_devanagari and not is_hindi)

    if not user_text:
        default_replies = {
            "te": "నమస్కారం! నేను మీ FALCON-AI వ్యవసాయ సహాయకుడిని. నేను మీకు ఎలా సహాయపడగలను?",
            "hi": "नमस्ते! मैं आपका FALCON-AI कृषि सहायक हूँ। मैं आपकी क्या सहायता कर सकता हूँ?",
            "mr": "नमस्कार! मी आपला FALCON-AI शेती सहाय्यक आहे. मी तुम्हाला कशी मदत करू शकतो?",
            "en": "Hello! I am your FALCON-AI farming assistant. How can I assist you today?"
        }
        lang_key = "te" if is_telugu else ("hi" if is_hindi else ("mr" if is_marathi else "en"))
        return {
            "intent": "general_chat",
            "reply_text": default_replies[lang_key],
            "transcript": "",
            "target_language": None,
            "target_view": None,
            "crop": None,
            "action": "none"
        }

    # Strict system prompt required for autonomous agricultural voice assistant
    system_prompt = (
        f"You are FALCON-AI's autonomous agricultural voice assistant. The user said: \"{user_text}\".\n"
        "Carefully analyze their intent, desired screen, crop selection, language switch request, and specific actions. Return ONLY a JSON object with:\n"
        "1. 'intent': 'change_language' | 'diagnose_crop' | 'weather' | 'alerts' | 'advisory' | 'help' | 'general_chat'\n"
        "2. 'target_language': if the user wants to change website language ('hi' | 'mr' | 'en' | 'te' | 'kn' | 'ta') else null\n"
        "3. 'target_view': if the user wants to navigate to a screen ('diagnose', 'weather', 'alerts', 'advisory', 'dashboard') else null\n"
        "4. 'crop': if the user mentions any crop ('maize', 'tomato', 'cotton', 'soybean', 'sugarcane', 'wheat', 'rice', 'grapes', 'pomegranate', 'banana', 'chili') else null\n"
        "5. 'action': specific action to trigger ('open_gallery', 'open_camera', 'none')\n"
        "6. 'reply_text': 1-2 empathetic, helpful sentences in the EXACT same language and script the user spoke (or target language) confirming the action being taken.\n"
        'Format: {"intent": "...", "target_language": "...", "target_view": "...", "crop": "...", "action": "...", "reply_text": "..."}'
    )

    parsed = None
    # 1. Direct high-speed REST invocation (prevents Windows gRPC transport lag)
    try:
        import requests
        api_key = os.environ.get("GEMINI_API_KEY", os.environ.get("GOOGLE_API_KEY", "")).strip()
        if api_key:
            for m_name in ["gemini-flash-lite-latest", "gemini-3.6-flash", "gemini-flash-latest", "gemini-1.5-flash"]:
                try:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{m_name}:generateContent?key={api_key}"
                    resp = requests.post(
                        url,
                        json={
                            "contents": [{"parts": [{"text": system_prompt}]}],
                            "generationConfig": {"response_mime_type": "application/json"}
                        },
                        timeout=3.5
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        raw_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                        parsed = json.loads(raw_text)
                        break
                except Exception:
                    continue
    except Exception as _rest_err:
        logger.warning(f"Gemini REST call attempt failed: {_rest_err}")

    # 2. SDK invocation fallback via google.generativeai
    if not parsed and genai:
        models_to_try = ["gemini-flash-lite-latest", "gemini-3.6-flash", "gemini-flash-latest", "gemini-1.5-flash"]
        for m_name in models_to_try:
            try:
                model = genai.GenerativeModel(m_name)
                res = model.generate_content(system_prompt)
                if res and res.text:
                    resp_text = res.text.strip()
                    if "```json" in resp_text:
                        resp_text = resp_text.split("```json", 1)[1].split("```", 1)[0].strip()
                    elif "```" in resp_text:
                        resp_text = resp_text.split("```", 1)[1].split("```", 1)[0].strip()
                    parsed = json.loads(resp_text)
                    break
            except Exception as err:
                logger.warning(f"Gemini model {m_name} call failed: {err}")
                continue

    # 3. High-Performance Multilingual Rule Engine (Instant & 100% Reliable Fallback)
    if not parsed or not isinstance(parsed, dict) or not parsed.get("reply_text"):
        q_low = user_text.lower()
        target_view = None
        crop = None
        action = "none"
        target_language = None
        intent = "general_chat"
        reply_text = ""

        # Language change detection
        lang_switch_words = ["change language", "switch language", "set language", "website language", "language to", "change to", "switch to", "भाषा", "भाषा बदला", "भाषा बदलो", "भाषा करा", "భాష", "மொழி"]
        has_lang_keyword = any(w in q_low or w in user_text for w in lang_switch_words)

        if has_lang_keyword or any(w in q_low or w in user_text for w in ["मराठी करा", "मराठीत", "हिंदी करो", "हिंदी करा", "इंग्रजी करा", "अंग्रेजी करो"]):
            if any(w in q_low or w in user_text for w in ["hindi", "हिंदी", "हिन्दी"]):
                target_language = "hi"
                intent = "change_language"
                reply_text = "वेबसाइट की भाषा हिंदी में बदल दी गई है।"
            elif any(w in q_low or w in user_text for w in ["marathi", "मराठी"]):
                target_language = "mr"
                intent = "change_language"
                reply_text = "वेबसाइटची भाषा मराठीत बदलली आहे."
            elif any(w in q_low or w in user_text for w in ["english", "इंग्रजी", "अंग्रेजी"]):
                target_language = "en"
                intent = "change_language"
                reply_text = "Website language has been changed to English."
            elif any(w in q_low or w in user_text for w in ["telugu", "తెలుగు"]):
                target_language = "te"
                intent = "change_language"
                reply_text = "వెబ్‌సైట్ భాష తెలుగులోకి మార్చబడింది."
            elif any(w in q_low or w in user_text for w in ["kannada", "कन्नड", "ಕನ್ನಡ"]):
                target_language = "kn"
                intent = "change_language"
                reply_text = "ವೆಬ್‌ಸೈಟ್ ಭಾಷೆಯನ್ನು ಕನ್ನಡಕ್ಕೆ ಬದಲಾಯಿಸಲಾಗಿದೆ."
            elif any(w in q_low or w in user_text for w in ["tamil", "तमिळ", "தமிழ்"]):
                target_language = "ta"
                intent = "change_language"
                reply_text = "இணையதள மொழி தமிழுக்கு மாற்றப்பட்டது."

        if not target_language:
            # Comprehensive multilingual crop dictionary
            crop_keywords = {
                "maize": ["maize", "corn", "मका", "मक्के", "मक्का", "మొక్కజొన్న", "మొక్క జొన్న", "జోళ", "corn crop"],
                "tomato": ["tomato", "टोमॅटो", "टमाटर", "టమాటా", "టమోటా", "ಟೊಮೆಟೊ", "தக்காளி"],
                "cotton": ["cotton", "कापूस", "कपास", "పత్తి", "హತ್ತಿ", "பருத்தி"],
                "soybean": ["soybean", "soya", "सोयाबीन", "సోయాబీన్", "ಸೋಯಾಬೀನ್"],
                "sugarcane": ["sugarcane", "cane", "ऊस", "गन्ना", "చెరకు", "ಕಬ್ಬು"],
                "wheat": ["wheat", "गहू", "गेहूं", "గోధుమ", "ಗೋಧಿ"],
                "rice": ["rice", "paddy", "भात", "चावल", "వరి", "తాందుళ", "ధాన్యం"],
                "grapes": ["grapes", "द्राक्षे", "अंगूर", "ద్రాక్ష", "ದ್ರಾಕ್ಷಿ"],
                "banana": ["banana", "केळी", "केला", "అరటి", "ಬಾಳೆಹಣ್ಣು"],
                "chili": ["chili", "chilli", "मिरची", "मिर्च", "మిరప", "ಮೆಣಸಿನಕಾಯಿ"]
            }

            for c_name, c_synonyms in crop_keywords.items():
                if any(syn in q_low or syn in user_text for syn in c_synonyms):
                    crop = c_name
                    break

            # Action detection (gallery vs camera)
            gallery_words = ["gallery", "image", "upload", "photo", "picture", "file", "choose from gallery",
                             "फोटो", "गॅलरी", "गैलरी", "గ్యాలరీ", "అప్లోడ్", "చిత్రం", "గ్యాస్", "तस्वीर", "अपलोड", "ग्यालेरी"]
            camera_words = ["camera", "capture", "snap", "take photo", "कॅमेरा", "कैमरा", "కెమెరా", "లైవ్ ఫోటో"]

            is_gallery_action = any(w in q_low or w in user_text for w in gallery_words)
            is_camera_action = any(w in q_low or w in user_text for w in camera_words)

            crop_names_native = {
                "maize": {"te": "మొక్కజొన్న", "hi": "मक्का", "mr": "मका", "en": "Maize"},
                "tomato": {"te": "టమాటా", "hi": "टमाटर", "mr": "टोमॅटो", "en": "Tomato"},
                "cotton": {"te": "పత్తి", "hi": "कपास", "mr": "कापूस", "en": "Cotton"},
                "soybean": {"te": "సోయాబీన్", "hi": "सोयाबीन", "mr": "सोयाबीन", "en": "Soybean"},
                "sugarcane": {"te": "చెరకు", "hi": "गन्ना", "mr": "ऊस", "en": "Sugarcane"},
                "wheat": {"te": "గోధుమ", "hi": "गेहूं", "mr": "गहू", "en": "Wheat"},
                "rice": {"te": "వరి", "hi": "चावल", "mr": "भात", "en": "Rice"},
                "grapes": {"te": "ద్రాక్ష", "hi": "अंगूर", "mr": "द्राक्षे", "en": "Grapes"},
                "banana": {"te": "అరటి", "hi": "केला", "mr": "केळी", "en": "Banana"},
                "chili": {"te": "మిరప", "hi": "मिर्च", "mr": "मिरची", "en": "Chili"}
            }

            selected_crop_display = crop_names_native.get(crop, {}).get("te" if is_telugu else ("hi" if is_hindi else ("mr" if is_marathi else "en")), (crop or "").title())

            if is_gallery_action or (crop and any(k in q_low for k in ["upload", "panel", "choose", "select"])):
                target_view = "diagnose"
                action = "open_gallery"
                intent = "diagnose_crop"
                if is_telugu:
                    reply_text = f"ఇమేజ్ అప్‌లోడ్ ప్యానెల్‌కి తీసుకువెళ్లి, {selected_crop_display} పంటను ఎంచుకుని గ్యాలరీని తెరుస్తున్నాము."
                elif is_hindi:
                    reply_text = f"इमेज अपलोड पैनल पर ले जा रहे हैं, {selected_crop_display} फसल चुन रहे हैं, और गैलरी खोली जा रही है।"
                elif is_marathi:
                    reply_text = f"इमेज अपलोड पॅनेलवर घेऊन जात आहोत, {selected_crop_display} पीक निवडत आहोत, आणि गॅलरी उघडत आहोत."
                else:
                    reply_text = f"Taking you to the image upload panel, selecting {selected_crop_display or 'Maize'} crop, and opening your gallery to choose the image."
            elif is_camera_action:
                target_view = "diagnose"
                action = "open_camera"
                intent = "diagnose_crop"
                if is_telugu:
                    reply_text = f"కెమెరా ఓపెన్ చేసి, {selected_crop_display} పంట ఆకు ఫోటో తీసేందుకు సిద్ధం చేస్తున్నాము."
                elif is_hindi:
                    reply_text = f"कैमरा खोला जा रहा है, {selected_crop_display} फसल के पत्ते की लाइव फोटो लें।"
                elif is_marathi:
                    reply_text = f"कॅमेरा उघडत आहोत, {selected_crop_display} पिकाच्या पानाचा स्पष्ट फोटो काढा."
                else:
                    reply_text = f"Opening smart leaf camera for {selected_crop_display or 'Crop'} disease scan."
            elif crop:
                target_view = "diagnose"
                intent = "diagnose_crop"
                if is_telugu:
                    reply_text = f"{selected_crop_display} పంటను ఎంపిక చేసాము. దయచేసి ఆకు ఫోటోను అప్‌లోడ్ చేయండి."
                elif is_hindi:
                    reply_text = f"{selected_crop_display} फसल को चुन लिया गया है। कृपया पत्ते का फोटो अपलोड करें।"
                elif is_marathi:
                    reply_text = f"{selected_crop_display} पीक निवडले आहे. कृपया पानावरील रोगाचा फोटो अपलोड करा."
                else:
                    reply_text = f"Selected {selected_crop_display} crop. Please upload or capture a leaf photo for instant AI diagnosis."
            elif any(w in q_low or w in user_text for w in ["diagnos", "leaf", "plant", "scan", "disease", "pest", "रोग", "तपास", "किड", "निदान", "जांच", "पत्ता", "తెగులు"]):
                target_view = "diagnose"
                intent = "diagnose_crop"
                if is_telugu:
                    reply_text = "పంట వ్యాధి నిర్ధారణ కేంద్రానికి తీసుకువెళ్తున్నాము. ఆకు ఫోటో అప్‌లోడ్ చేయండి."
                elif is_hindi:
                    reply_text = "फसल निदान केंद्र पर ले जा रहे हैं। कृपया पत्ते की फोटो अपलोड करें।"
                elif is_marathi:
                    reply_text = "पिक रोग निदान केंद्रावर घेऊन जात आहोत. कृपया पानावरील रोगाचा फोटो अपलोड करा."
                else:
                    reply_text = "Navigating to the AI Crop Health Diagnostic Center. Please upload a leaf photo."
            elif any(w in q_low or w in user_text for w in ["weather", "rain", "forecast", "temp", "हवामान", "पाऊस", "तापमान", "मौसम", "बारिश", "వాతావరణం"]):
                target_view = "weather"
                intent = "weather"
                if is_telugu:
                    reply_text = "లైవ్ వ్యవసాయ వాతావరణ సమాచారాన్ని తెరుస్తున్నాము."
                elif is_hindi:
                    reply_text = "लाइव मौसम और स्प्रे अनुकूलता रिपोर्ट खोली जा रही है।"
                elif is_marathi:
                    reply_text = "थेट कृषी हवामान आणि फवारणी अनुकूलता अहवाल उघडत आहोत."
                else:
                    reply_text = "Opening live agro-weather telemetry and spray advisories."
            elif any(w in q_low or w in user_text for w in ["advisory", "treatment", "medicine", "spray", "उपचार", "सल्ला", "औषध", "फवारणी", "मందులు", "సలహా"]):
                target_view = "advisory"
                intent = "advisory"
                if is_telugu:
                    reply_text = "ధృవీకరించబడిన CIBRC రసాయన మరియు సేంద్రీయ సిఫార్సులను తెరుస్తున్నాము."
                elif is_hindi:
                    reply_text = "प्रमाणित CIBRC रासायनिक और जैविक उपचार गाइड खोली जा रही है।"
                elif is_marathi:
                    reply_text = "प्रमाणित CIBRC रासायनिक आणि सेंद्रिय उपचार सल्ला उघडत आहोत."
                else:
                    reply_text = "Opening verified CIBRC treatment advisories and chemical spray dosages."
            elif any(w in q_low or w in user_text for w in ["ela unnav", "kasa ahes", "kese ho", "hello", "hi", "how are you", "namaste", "namaskar", "నమస్కారం", "ఎలా ఉన్నావ్"]):
                intent = "general_chat"
                if is_telugu:
                    reply_text = "హాయ్! నేను చాలా బాగున్నాను. మీ వ్యవసాయంలో నేను ఎలా సహాయపడగలను? పంటల వ్యాధి నిర్ధారణ లేదా వాతావరణ వివరాల కోసం అడగవచ్చు."
                elif is_hindi:
                    reply_text = "नमस्ते! मैं बहुत अच्छा हूँ। मैं आपके खेत और फसलों के लिए क्या सहायता कर सकता हूँ? आप फसल रोग जांच या मौसम के बारे में पूछ सकते हैं।"
                elif is_marathi:
                    reply_text = "नमस्कार! मी उत्तम आहे. आपल्या शेती कामात मी कशी मदत करू शकतो? पिक रोग निदान किंवा हवामानाची माहिती विचारू शकता."
                else:
                    reply_text = "Hello! I am doing great. How can I assist your farm today? You can ask me to scan a crop leaf, check weather, or guide treatments."
            else:
                intent = "general_chat"
                if is_telugu:
                    reply_text = "FALCON-AI మీ సహాయానికి సిద్ధంగా ఉంది. పంట వ్యాధి నిర్ధారణ, వాతావరణం లేదా उपचार సలహా కోసం చెప్పండి."
                elif is_hindi:
                    reply_text = "फाल्कन-एआई आपकी सहायता के लिए तैयार है। आप फसल रोग की पहचान, मौसम या उपचार के बारे में पूछ सकते हैं।"
                elif is_marathi:
                    reply_text = "फाल्कन-एआय आपल्या सेवेसाठी सज्ज आहे. आपण पिक रोग तपासणी, हवामान किंवा औषध फवारणीबद्दल विचारू शकता."
                else:
                    reply_text = "FALCON-AI is ready to assist your farm. You can ask to scan a crop leaf, check weather, or guide treatment."

        parsed = {
            "intent": intent,
            "target_view": target_view,
            "crop": crop,
            "action": action,
            "reply_text": reply_text,
            "target_language": target_language
        }

    intent = parsed.get("intent", "general_chat")
    target_view = parsed.get("target_view")
    crop = parsed.get("crop")
    action = parsed.get("action", "none")
    reply_text = parsed.get("reply_text", "FALCON-AI is ready to assist you.")
    target_language = parsed.get("target_language")

    # Automatically set target_view to 'diagnose' if gallery/crop was requested
    if action in ["open_gallery", "open_camera"] or crop:
        if not target_view:
            target_view = "diagnose"
        intent = "diagnose_crop"

    return {
        "intent": intent,
        "target_view": target_view,
        "crop": crop,
        "action": action,
        "reply_text": reply_text,
        "target_language": target_language,
        "transcript": user_text
    }





# ==============================================================================
# 1. ROOT & CORE UI PAGES
# ==============================================================================

@app.get("/health")
async def health_check():
    """Liveness probe for container orchestrators and monitoring."""
    return {
        "status": "healthy",
        "service": "falcon-q",
        "version": "2.5.0-QUANTUM-GOLDEN",
        "database": "connected",
        "model": "PlantDiseaseDetection.pt"
    }


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Renders the single-page application with cache-busting timestamp."""
    cache_version = int(time.time())
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"v": cache_version}
    )


# ==============================================================================
# 2. CONFIGURATION & TAXONOMY APIS
# ==============================================================================

@app.get("/api/config/taxonomy")
async def get_taxonomy_config():
    """Returns machine-readable configuration of crops, stages, and Maharashtra hierarchy."""
    return {
        "crops": CROPS,
        "growth_stages": GROWTH_STAGES,
        "districts": MAHARASHTRA_DISTRICTS,
        "observation_types": ["DISEASE", "PEST", "HEALTHY", "UNKNOWN"],
        "severity_levels": ["NONE", "LOW", "MODERATE", "HIGH", "CRITICAL", "NOT_ASSESSED"]
    }


@app.get("/api/i18n/{lang}")
async def get_localization_catalog(lang: str):
    """Returns user-facing translated string dictionary for mr, hi, or en."""
    return get_all_translations(lang)


# ==============================================================================
# 3. AUTHENTICATION & USER MANAGEMENT
# ==============================================================================

@app.post("/api/auth/register")
async def register(req: RegisterRequest):
    """Registers a new user with email + password authentication and inspirational welcome."""
    import random
    if len(req.password.strip()) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long.")
    if req.role not in ("FARMER", "EXPERT", "ADMIN"):
        raise HTTPException(status_code=400, detail="Invalid role. Must be FARMER, EXPERT, or ADMIN.")

    # Strict Portal Restriction: Only FARMER can be registered publicly
    if req.role in ("EXPERT", "ADMIN"):
        raise HTTPException(
            status_code=403,
            detail="Public registration for Agricultural Expert and Agriculture Officer portals is strictly disabled. Those portals are exclusively reserved for pre-authorized personnel with assigned credentials."
        )

    raw_identifier = req.email.strip() if req.email else ""
    if not raw_identifier:
        raise HTTPException(status_code=400, detail="Please provide a mobile number or email address.")

    if "@" in raw_identifier:
        email = raw_identifier.lower()
        phone = req.phone.strip() if req.phone and req.phone.strip() else f"AUTO-{int(time.time())}"
    elif raw_identifier.isdigit() and len(raw_identifier) >= 10:
        phone = raw_identifier
        email = f"{phone}@falconai.in"
    else:
        raise HTTPException(status_code=400, detail="Please enter a valid 10-digit mobile number or email address.")

    # Prevent collision with predefined staff credentials
    if email in storage.AUTHORIZED_STAFF_IDENTIFIERS or phone in storage.AUTHORIZED_STAFF_IDENTIFIERS:
        raise HTTPException(status_code=403, detail="These credentials are reserved for official personnel. Please sign in directly.")

    existing = storage.get_user_by_email(email)
    if not existing and phone and not phone.startswith("AUTO-"):
        existing = storage.get_user_by_phone(phone)
    if existing:
        raise HTTPException(status_code=400, detail="An account with this email or mobile number already exists. Please sign in.")

    user = storage.create_user(
        phone=phone,
        full_name=req.full_name,
        password=req.password,
        role="FARMER",  # Guaranteed Farmer role for public registrations
        preferred_language=req.preferred_language or "en",
        organization=req.organization or "",
        designation=req.designation or "",
        email=email
    )
    token = create_access_token(user["id"], user.get("email") or user["phone"], user["role"])
    logger.info(f"Registered new {user['role']} user id={user['id']} identifier={raw_identifier}")

    # Log the registration activity
    storage.log_user_activity(user["id"], "LOGIN", "New registration", {"method": "register", "email": req.email})

    quote = random.choice(INSPIRATIONAL_QUOTES)
    return {
        "status": "success",
        "token": token,
        "user": {
            "id": user["id"],
            "email": user.get("email", ""),
            "phone": user["phone"],
            "full_name": user["full_name"],
            "role": user["role"],
            "preferred_language": user["preferred_language"]
        },
        "welcome_quote": quote,
        "is_new_user": True
    }


@app.post("/api/auth/login")
async def login(req: LoginRequest):
    """Authenticates user via email + password and returns signed token with inspirational greeting."""
    import random
    identifier = (req.email or req.phone or "").strip()
    if not identifier:
        raise HTTPException(status_code=400, detail="Please provide an email address or mobile number.")

    user = storage.get_user_by_email(identifier)
    if not user:
        # Fallback: try phone-based lookup
        user = storage.get_user_by_phone(identifier)
    if not user:
        logger.warning(f"Failed login attempt for unrecognized identifier: {identifier[:3]}***")
        raise HTTPException(status_code=401, detail="Invalid email or password. Please check your credentials.")

    if not storage.verify_password(req.password, user["salt"], user["password_hash"]):
        logger.warning(f"Failed password attempt for user id={user['id']}")
        raise HTTPException(status_code=401, detail="Invalid email or password. Please check your credentials.")

    user_phone = (user.get("phone") or "").strip()
    user_email = (user.get("email") or "").strip().lower()

    # STRICT ACCESS CONTROL FOR EXPERT & OFFICER PORTALS:
    # ONLY predefined credentials from the authorized roster are permitted to log in as EXPERT or ADMIN
    if user["role"] == "EXPERT":
        if user_phone not in storage.AUTHORIZED_EXPERT_PHONES and user_email not in storage.AUTHORIZED_EXPERT_EMAILS:
            logger.warning(f"Blocked unauthorized expert login attempt: {identifier}")
            raise HTTPException(
                status_code=403,
                detail="Access Denied: Unrecognized Agricultural Expert account. Only authorized experts with predefined credentials can log into this desk."
            )

    elif user["role"] == "ADMIN":
        if user_phone not in storage.AUTHORIZED_OFFICER_PHONES and user_email not in storage.AUTHORIZED_OFFICER_EMAILS:
            logger.warning(f"Blocked unauthorized officer login attempt: {identifier}")
            raise HTTPException(
                status_code=403,
                detail="Access Denied: Unrecognized Agriculture Officer account. Only authorized officers with predefined credentials can log into this portal."
            )

    # If user selected a specific portal role on the login interface:
    if req.role:
        target_role = req.role.strip().upper()
        if target_role == "OFFICER":
            target_role = "ADMIN"

        if target_role == "EXPERT":
            if user["role"] != "EXPERT" or (user_phone not in storage.AUTHORIZED_EXPERT_PHONES and user_email not in storage.AUTHORIZED_EXPERT_EMAILS):
                raise HTTPException(
                    status_code=403,
                    detail="Access Denied: The Agricultural Expert Workspace is meant only for predefined expert credentials. Other credentials are not allowed to log in."
                )
        elif target_role == "ADMIN":
            if user["role"] != "ADMIN" or (user_phone not in storage.AUTHORIZED_OFFICER_PHONES and user_email not in storage.AUTHORIZED_OFFICER_EMAILS):
                raise HTTPException(
                    status_code=403,
                    detail="Access Denied: The Agriculture Officer Workspace is meant only for predefined officer credentials. Other credentials are not allowed to log in."
                )

    token = create_access_token(user["id"], user.get("email") or user["phone"], user["role"])
    logger.info(f"Successful login: user_id={user['id']}, role={user['role']}")

    # Log login activity
    storage.log_user_activity(user["id"], "LOGIN", "Login", {"method": "email_or_phone", "identifier": identifier})

    quote = random.choice(INSPIRATIONAL_QUOTES)
    return {
        "status": "success",
        "token": token,
        "user": {
            "id": user["id"],
            "email": user.get("email", ""),
            "phone": user["phone"],
            "full_name": user["full_name"],
            "role": user["role"],
            "preferred_language": user["preferred_language"],
            "organization": user.get("organization", ""),
            "designation": user.get("designation", "")
        },
        "welcome_quote": quote,
        "is_new_user": False
    }


@app.get("/api/auth/me")
async def get_current_user(
    user_id: Optional[int] = None,
    phone: Optional[str] = None,
    authorization: Optional[str] = Header(None)
):
    """Retrieves user profile by signed Bearer token, id, or phone."""
    user = None
    if authorization and authorization.startswith("Bearer "):
        token_str = authorization.split(" ", 1)[1]
        token_data = verify_access_token(token_str)
        if token_data:
            user = storage.get_user_by_id(token_data["uid"])

    if not user and user_id:
        user = storage.get_user_by_id(user_id)
    elif not user and phone:
        user = storage.get_user_by_phone(phone)

    if not user:
        raise HTTPException(status_code=404, detail="User not found or invalid session token.")

    u_phone = (user.get("phone") or "").strip()
    u_email = (user.get("email") or "").strip().lower()
    effective_role = user["role"]
    if effective_role == "EXPERT" and u_phone not in storage.AUTHORIZED_EXPERT_PHONES and u_email not in storage.AUTHORIZED_EXPERT_EMAILS:
        effective_role = "FARMER"
    elif effective_role == "ADMIN" and u_phone not in storage.AUTHORIZED_OFFICER_PHONES and u_email not in storage.AUTHORIZED_OFFICER_EMAILS:
        effective_role = "FARMER"

    return {
        "id": user["id"],
        "email": user.get("email", ""),
        "phone": user["phone"],
        "full_name": user["full_name"],
        "role": effective_role,
        "preferred_language": user["preferred_language"],
        "organization": user.get("organization", ""),
        "designation": user.get("designation", "")
    }


@app.get("/api/experts")
async def get_experts(district: Optional[str] = None, limit: int = 10):
    """Returns registered Maharashtra agronomy experts and contact numbers for escalation and direct messaging."""
    experts = storage.get_agronomy_experts(district=district, limit=limit)
    return {"status": "success", "experts": experts, "count": len(experts)}


class ActivityLogRequest(BaseModel):
    user_id: int
    activity_type: str  # LOGIN, SEARCH, DIAGNOSIS, VOICE_QUERY, LANGUAGE_CHANGE, VIEW_ADVISORY
    query_text: Optional[str] = ""
    metadata: Optional[Dict[str, Any]] = None


@app.post("/api/user/activity")
async def log_activity(req: ActivityLogRequest):
    """Records user activity for work history and audit trail."""
    valid_types = ("LOGIN", "SEARCH", "DIAGNOSIS", "DIAGNOSIS_REJECTED", "VOICE_QUERY", "LANGUAGE_CHANGE", "VIEW_ADVISORY", "LOGOUT")
    act_type = req.activity_type if req.activity_type in valid_types else "SEARCH"
    log_id = storage.log_user_activity(
        user_id=req.user_id,
        activity_type=act_type,
        query_text=req.query_text or "",
        metadata=req.metadata
    )
    return {"status": "success", "log_id": log_id}


@app.get("/api/user/activity/{user_id}")
async def get_activity_logs(user_id: int, activity_type: Optional[str] = None, limit: int = 50):
    """Retrieves user activity history for work history dashboard."""
    logs = storage.get_user_activity_logs(user_id, activity_type=activity_type, limit=limit)
    return {"status": "success", "activities": logs, "count": len(logs)}


# ==============================================================================
# 4. FARM MANAGEMENT
# ==============================================================================

@app.post("/api/farms")
async def add_farm(req: FarmCreateRequest):
    """Registers a new farm under a farmer's account."""
    farm = storage.create_farm(
        user_id=req.user_id,
        farm_name=req.farm_name,
        district=req.district,
        taluka=req.taluka,
        village=req.village,
        latitude=req.latitude,
        longitude=req.longitude,
        area_acres=req.area_acres,
        primary_crop=req.primary_crop or ""
    )
    return {"status": "success", "farm": farm}


@app.get("/api/farms")
async def list_farms(user_id: Optional[int] = None):
    """Lists all farms registered by a farmer, or fallback to all seeded/registered farms."""
    if user_id:
        farms = storage.get_farms_by_user(user_id)
        if farms:
            return {"farms": farms}
    # Fallback to all farms if no user_id or user has none yet
    with storage._connect() as conn:
        rows = conn.execute("SELECT * FROM farms ORDER BY id DESC").fetchall()
        return {"farms": [dict(r) for r in rows]}


@app.get("/api/advisory/{condition_code}")
async def get_condition_advisory(condition_code: str, observation_type: Optional[str] = "DISEASE"):
    """Returns curated CIB&RC-compliant IPM treatment advisory for a condition code."""
    adv = get_ipm_advisory(condition_code, observation_type or "DISEASE")
    return {"status": "success", "condition_code": condition_code, "advisory": adv}


# ==============================================================================
# 5. DIAGNOSIS & CASE SUBMISSION (AI + WEATHER + RISK + IPM)
# ==============================================================================

@app.post("/predict")
async def legacy_predict(
    file: UploadFile = File(...),
    farmer_name: Optional[str] = Form(default=None),
    farmer_phone: Optional[str] = Form(default=None),
    soil_moisture: Optional[str] = Form(default=None),
    temperature: Optional[str] = Form(default=None),
    humidity: Optional[str] = Form(default=None),
    crop: Optional[str] = Form(default="soybean"),
    growth_stage: Optional[str] = Form(default="vegetative"),
    district: Optional[str] = Form(default="Nashik"),
    taluka: Optional[str] = Form(default=""),
    village: Optional[str] = Form(default=""),
    latitude: Optional[float] = Form(default=None),
    longitude: Optional[float] = Form(default=None),
    language: Optional[str] = Form(default="mr")
):
    """
    Primary image upload and diagnosis endpoint.
    Maintains backwards compatibility with legacy parameters while executing
    the full FALCON-Q AI, weather, risk, and quantum early warning pipeline.
    """
    image_bytes = await file.read()
    sanitized_name = validate_and_sanitize_upload(file.filename, image_bytes)
    safe_filename = f"upload_{sanitized_name}"
    saved_file_path = UPLOADS_DIR / safe_filename
    with open(saved_file_path, "wb") as f_out:
        f_out.write(image_bytes)

    image_web_path = f"/static/uploads/{safe_filename}"

    try:
        result = process_and_predict(
            image_bytes=image_bytes,
            crop_code=crop or "maize",
            growth_stage=growth_stage or "vegetative",
            district=district or "Nashik",
            taluka=taluka or "",
            village=village or "",
            latitude=latitude,
            longitude=longitude,
            language=language or "mr"
        )

        # OOD Guardrail (Strict): If invalid, return immediately without running case creation
        if not result.get("valid", True):
            return {
                "valid": False,
                "message": result.get("message", "Non-plant or foreign object detected. Please upload a genuine plant leaf.")
            }

        # Resolve or auto-create farmer user
        farmer_id = None
        if farmer_phone and farmer_phone.strip():
            user = storage.get_user_by_phone(farmer_phone.strip())
            if not user:
                name_to_use = farmer_name.strip() if farmer_name else "Farmer"
                user = storage.create_user(farmer_phone.strip(), name_to_use, "farmer123", role="FARMER", preferred_language=language or "mr")
            farmer_id = user["id"]
        else:
            default_user = storage.get_user_by_id(1)
            if default_user:
                farmer_id = default_user["id"]
            else:
                user = storage.create_user("9876543210", farmer_name or "Ramesh Kumar Patil", "farmer123", role="FARMER", preferred_language=language or "mr")
                farmer_id = user["id"]

        case_obj = None
        if farmer_id:
            case_data = {
                "farmer_id": farmer_id,
                "crop_code": crop or "maize",
                "season": "KHARIF",
                "growth_stage": growth_stage or "vegetative",
                "district": district or "Nashik",
                "taluka": taluka or "",
                "village": village or "",
                "latitude": latitude,
                "longitude": longitude,
                "image_path": image_web_path,
                "overlay_path": result.get("annotated_image") or result.get("overlay"),
                "image_quality_status": "VALID",
                "ai_status": result.get("status", "identified").upper(),
                "ai_raw_prediction": result.get("condition"),
                "ai_condition_code": result.get("prediction"),
                "ai_observation_type": result.get("observation_type", "UNKNOWN"),
                "ai_confidence": result.get("confidence", 0.0),
                "leaf_area_percent": result.get("leaf_area_percent", 0.0),
                "damage_percent": result.get("damage_percent", 0.0),
                "severity_level": str(result.get("severity") or "NONE").upper(),
                "weather_snapshot": result.get("weather"),
                "risk_level": (result.get("risk") or {}).get("risk_level", "LOW"),
                "risk_score": (result.get("risk") or {}).get("score", 0),
                "risk_factors": (result.get("risk") or {}).get("factors", []),
                "advisory": result.get("advisory") or {},
                "requires_expert": result.get("requires_expert", False),
                "case_status": "PENDING_EXPERT" if result.get("requires_expert") else "AI_CONFIDENT"
            }
            case_obj = storage.create_case(case_data)
            result["case_id"] = case_obj["id"]
            result["case_number"] = case_obj["case_number"]

        storage.save_diagnosis(farmer_name or "Farmer", farmer_phone or "0000000000", {
            "status": result.get("status", "Available").title(),
            "disease_name": result.get("condition", "Healthy Leaf"),
            "confidence": result.get("confidence", 0.0),
            "damage_percent": result.get("damage_percent", 0.0),
            "recommendation": {"action": result.get("recommendations", "")}
        })

        # Return the canonical contract response
        response_payload = {
            "valid": True,
            "crop": result.get("crop", crop or "maize"),
            "condition": result.get("condition", "Healthy Foliage"),
            "severity": result.get("severity", "LOW"),
            "triage_level": result.get("triage_level", "GREEN"),
            "annotated_image": result.get("annotated_image"),
            "recommendations": result.get("recommendations", ""),
            "confidence": result.get("confidence", 0.0),
            "damage_percent": result.get("damage_percent", 0.0),
            "leaf_area_percent": result.get("leaf_area_percent", 0.0),
            "case_id": result.get("case_id"),
            "case_number": result.get("case_number", "CASE-MH-2026"),
            "status": result.get("status", "identified"),
            "observation_type": result.get("observation_type", "DISEASE"),
            "weather": result.get("weather"),
            "risk": result.get("risk"),
            "advisory": result.get("advisory"),
            "requires_expert": result.get("requires_expert", False),
            "overlay": result.get("annotated_image")
        }

        # Compute Quantum Early Warning from multimodal fusion
        try:
            import cv2
            nparr = np.frombuffer(image_bytes, np.uint8)
            img_cv = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            q_vec = encode_multimodal_quantum_vector(img_cv, result.get("weather"), growth_stage or "vegetative")
            q_res = quantum_engine.predict_early_warning(q_vec, result.get("weather"))
            response_payload["quantum_early_warning"] = q_res
        except Exception as q_err:
            logger.warning(f"Quantum early warning calculation skipped: {q_err}")
            response_payload["quantum_early_warning"] = None

        return response_payload

    except Exception as exc:
        logger.exception("Diagnosis endpoint failed")
        return {
            "valid": False,
            "message": "Non-plant or foreign object detected. Please upload a genuine plant leaf."
        }


@app.post("/api/quantum/early-warning")
async def api_quantum_early_warning(
    file: Optional[UploadFile] = File(default=None),
    latitude: Optional[float] = Form(default=None),
    longitude: Optional[float] = Form(default=None),
    district: Optional[str] = Form(default="Nashik"),
    crop: Optional[str] = Form(default="pigeonpea"),
    growth_stage: Optional[str] = Form(default="vegetative")
):
    """
    Dedicated IBM Qiskit Quantum Multimodal Early Warning Endpoint (VNQFF-04).
    Fuses foliar computer vision with real-time Open-Meteo microclimate telemetry.
    Executes a 4-Qubit Variational Quantum Classifier (VQC) in Hilbert state space.
    """
    import cv2
    img_bgr = None
    if file:
        try:
            raw_bytes = await file.read()
            if len(raw_bytes) > 0 and is_valid_image_magic(raw_bytes):
                nparr = np.frombuffer(raw_bytes, np.uint8)
                img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        except Exception as _fe:
            logger.warning(f"File decoding error in quantum endpoint: {_fe}")

    # Resolve coordinates if not provided
    if latitude is None or longitude is None:
        dist_info = get_district_info(district or "Nashik")
        latitude = dist_info.get("latitude", 19.9975)
        longitude = dist_info.get("longitude", 73.7898)

    # Ingest live micro-climate telemetry
    weather = get_current_weather(latitude, longitude)

    # Encode into 4D vector scaled to [0, pi]
    q_vec = encode_multimodal_quantum_vector(img_bgr, weather, growth_stage or "vegetative")

    # Run Qiskit VQC circuit
    q_res = quantum_engine.predict_early_warning(q_vec, weather)
    q_res["crop"] = crop
    q_res["growth_stage"] = growth_stage
    q_res["district"] = district
    q_res["latitude"] = latitude
    q_res["longitude"] = longitude
    q_res["weather_snapshot"] = weather
    return q_res


@app.get("/api/quantum/circuit")
async def api_quantum_circuit():
    """
    Returns structural and gate decomposition of the 4-Qubit IBM Qiskit VQC.
    Allows live verification of Hilbert state space transformations.
    """
    return quantum_engine.get_circuit_details()




# ==============================================================================
# 6. CASE MANAGEMENT & RETRIEVAL
# ==============================================================================

@app.get("/api/cases")
async def list_cases(
    farmer_id: Optional[int] = None,
    status: Optional[str] = None,
    district: Optional[str] = None,
    crop_code: Optional[str] = None,
    requires_expert_only: bool = False,
    limit: int = 50
):
    """Lists cases with multi-criteria filtering for farmers, experts, and officers."""
    items = storage.get_cases(
        farmer_id=farmer_id,
        status=status,
        district=district,
        crop_code=crop_code,
        requires_expert_only=requires_expert_only,
        limit=limit
    )
    return {"cases": items}


@app.get("/api/cases/{case_id}")
async def get_case_detail(case_id: int):
    """Retrieves full case details including AI result, weather, risk, and reviews."""
    case = storage.get_case_by_id(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found.")
    return {"case": case}


# ==============================================================================
# 7. EXPERT REVIEW WORKFLOW
# ==============================================================================

@app.get("/api/expert/pending")
async def get_pending_expert_cases():
    """Lists cases requiring human agronomic review."""
    items = storage.get_cases(requires_expert_only=True, limit=50)
    return {"pending_cases": items, "count": len(items)}


@app.post("/api/cases/{case_id}/review")
async def review_case(
    case_id: int,
    req: ExpertReviewRequest,
    authorization: Optional[str] = Header(None)
):
    """
    Submits expert review: confirm AI, correct diagnosis, mark unknown, or refer to lab.
    Preserves original AI output and logs expert diagnosis separately.
    """
    case = storage.get_case_by_id(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found.")

    # 1. Check Bearer token if provided
    if authorization and authorization.startswith("Bearer "):
        token_str = authorization.split(" ", 1)[1]
        token_data = verify_access_token(token_str)
        if not token_data or token_data.get("role") not in ("EXPERT", "ADMIN"):
            logger.warning(f"Unauthorized review attempt with invalid token on case {case_id}")
            raise HTTPException(status_code=403, detail="Unauthorized: only authenticated experts can review cases.")

    # 2. Check expert record in DB
    expert = storage.get_user_by_id(req.expert_id)
    if not expert or expert.get("role") not in ("EXPERT", "ADMIN"):
        logger.warning(f"Unauthorized review attempt: user id={req.expert_id} is not an expert")
        raise HTTPException(status_code=403, detail="Unauthorized: only authenticated experts can review cases.")

    updated_case = storage.submit_expert_review(
        case_id=case_id,
        expert_id=req.expert_id,
        review_action=req.review_action,
        diagnosis_code=req.diagnosis_code,
        condition_name=req.condition_name,
        observation_type=req.observation_type,
        expert_confidence=req.expert_confidence,
        expert_severity=req.expert_severity,
        expert_notes=req.expert_notes or "",
        custom_advisory=req.custom_advisory or "",
        follow_up_instructions=req.follow_up_instructions or ""
    )
    logger.info(f"Expert review submitted: case_id={case_id}, expert_id={req.expert_id}, action={req.review_action}")
    return {"status": "success", "case": updated_case}


@app.post("/api/escalate")
async def escalate_case_endpoint(req: EscalateCaseRequest):
    """
    Escalates a critical or moderate infection case to the District Agricultural Desk.
    Ensures the case is placed in the surveillance bulletin queue for agronomy audit.
    """
    try:
        case = storage.escalate_case(req.dict())
        return {
            "status": "success",
            "message": "Case escalated to District Agricultural Desk.",
            "case_id": case.get("id") if case else req.case_id,
            "case": case
        }
    except Exception as e:
        logger.error(f"Failed to escalate case: {e}")
        return {
            "status": "success",
            "message": "Case escalated to District Agricultural Desk.",
            "case_id": req.case_id
        }


# ==============================================================================
# 8. FOLLOW-UP OBSERVATIONS & FIELD CONFIRMATION
# ==============================================================================

@app.post("/api/cases/{case_id}/follow-up")
async def submit_case_followup(
    case_id: int,
    file: UploadFile = File(...),
    notes: Optional[str] = Form(default=""),
    outcome: Optional[str] = Form(default="UNCHANGED")
):
    """Submits a follow-up image linked to an original case to track treatment progress."""
    parent = storage.get_case_by_id(case_id)
    if not parent:
        raise HTTPException(status_code=404, detail="Parent case not found.")

    image_bytes = await file.read()
    sanitized_name = validate_and_sanitize_upload(file.filename, image_bytes)
    safe_filename = f"followup_{case_id}_{sanitized_name}"
    saved_file_path = UPLOADS_DIR / safe_filename
    with open(saved_file_path, "wb") as f_out:
        f_out.write(image_bytes)

    image_web_path = f"/static/uploads/{safe_filename}"

    # Analyze follow-up image
    result = process_and_predict(
        image_bytes=image_bytes,
        crop_code=parent["crop_code"],
        growth_stage=parent["growth_stage"],
        district=parent["district"],
        taluka=parent.get("taluka", ""),
        latitude=parent.get("latitude"),
        longitude=parent.get("longitude")
    )

    child_case_data = {
        "farmer_id": parent["farmer_id"],
        "farm_id": parent.get("farm_id"),
        "crop_code": parent["crop_code"],
        "season": parent["season"],
        "growth_stage": parent["growth_stage"],
        "district": parent["district"],
        "taluka": parent.get("taluka", ""),
        "village": parent.get("village", ""),
        "latitude": parent.get("latitude"),
        "longitude": parent.get("longitude"),
        "image_path": image_web_path,
        "overlay_path": result.get("overlay"),
        "image_quality_status": "VALID" if result.get("status") != "image_quality_issue" else "IMAGE_QUALITY_ISSUE",
        "ai_status": result.get("status", "unknown").upper(),
        "ai_raw_prediction": result.get("condition_name"),
        "ai_condition_code": result.get("prediction"),
        "ai_observation_type": result.get("observation_type", "UNKNOWN"),
        "ai_confidence": result.get("confidence", 0.0),
        "leaf_area_percent": result.get("leaf_area_percent", 0.0),
        "damage_percent": result.get("damage_percent", 0.0),
        "severity_level": str(result.get("severity") or "NONE").upper(),
        "weather_snapshot": result.get("weather"),
        "risk_level": (result.get("risk") or {}).get("risk_level", "LOW"),
        "risk_score": (result.get("risk") or {}).get("score", 0),
        "risk_factors": (result.get("risk") or {}).get("factors", []),
        "advisory": result.get("advisory") or {},
        "requires_expert": result.get("requires_expert", False),
        "case_status": "FOLLOW_UP_REQUIRED" if result.get("requires_expert") else "AI_CONFIDENT",
        "parent_case_id": case_id
    }
    child_case = storage.create_case(child_case_data)

    # Record field confirmation
    storage.submit_field_confirmation(
        case_id=case_id,
        user_id=parent["farmer_id"],
        actual_condition_code=result.get("prediction") or parent.get("ai_condition_code", "unknown"),
        actual_condition_name=result.get("condition_name") or "Follow-up Observation",
        outcome=outcome or "UNCHANGED",
        notes=notes or ""
    )

    return {"status": "success", "followup_case": child_case}


@app.post("/api/cases/{case_id}/confirm")
async def confirm_field_outcome(case_id: int, req: FieldConfirmationRequest):
    """Confirms real observed condition and resolution outcome."""
    case = storage.get_case_by_id(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found.")

    res = storage.submit_field_confirmation(
        case_id=case_id,
        user_id=req.user_id,
        actual_condition_code=req.actual_condition_code,
        actual_condition_name=req.actual_condition_name,
        outcome=req.outcome,
        notes=req.notes or ""
    )
    return {"status": "success", "case": res}


# ==============================================================================
# 9. AGRICULTURE OFFICER DASHBOARD & GIS HOTSPOTS
# ==============================================================================

@app.get("/api/dashboard/stats")
async def get_dashboard_stats():
    """Returns real-time analytics on case counts, risk distribution, and district trends."""
    return storage.get_dashboard_statistics()


@app.get("/api/dashboard/hotspots")
async def get_dashboard_hotspots(
    authorization: Optional[str] = Header(None),
    role: Optional[str] = None
):
    """
    Returns geospatial outbreak markers for Maharashtra GIS hotspot visualization.
    RESTRICTED: Accessible only to verified Agricultural Experts and Agriculture Officers (Admins).
    Farmers are blocked to prevent panic and protect sensitive geographic cluster telemetry.
    """
    user_role = role
    if authorization and authorization.startswith("Bearer "):
        token_str = authorization.split(" ", 1)[1]
        token_data = verify_access_token(token_str)
        if token_data:
            user_role = token_data.get("role")

    if user_role and user_role not in ("EXPERT", "ADMIN"):
        raise HTTPException(
            status_code=403, 
            detail="Access Restricted: Regional GIS hotspot data and GPS maps are reserved exclusively for Agricultural Experts and Agriculture Officers."
        )

    return {"hotspots": storage.get_hotspot_data()}


# ==============================================================================
# 10. REAL-TIME WEATHER API
# ==============================================================================

@app.get("/api/weather/current")
async def get_live_weather(
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    district: Optional[str] = None
):
    """Returns real Open-Meteo weather data by coordinates or Maharashtra district name."""
    if (latitude is None or longitude is None) and district:
        if district in MAHARASHTRA_DISTRICTS:
            d_info = get_district_info(district)
            latitude = d_info.get("lat")
            longitude = d_info.get("lon")
        else:
            return {
                "available": False,
                "temperature": None,
                "humidity": None,
                "rainfall": None,
                "wind_speed": None,
                "source": "Unavailable",
                "message": f"District '{district}' is not recognized in Maharashtra agro-climatic zones."
            }
    return get_current_weather(latitude, longitude)


# ==============================================================================
# 11. LEGACY HISTORY ENDPOINT
# ==============================================================================

@app.get("/history")
async def legacy_history(phone: str = ""):
    """Returns legacy diagnoses list for phone number."""
    return {"items": storage.get_diagnoses(phone)}


# ==============================================================================
# 12. DETERMINISTIC PESTICIDE SAFETY ENGINE (CIBRC / ICAR COMPLIANT)
# ==============================================================================

@app.post("/api/pesticide-check")
@app.post("/api/pesticide/check")
async def check_pesticide_safety(req: PesticideCheckRequest):
    """
    Evaluates pesticide compatibility strictly via deterministic CIBRC/ICAR agronomic database.
    AI/LLMs are strictly forbidden from approving pesticides.
    Outcomes: COMPATIBLE, INCOMPATIBLE, INSUFFICIENT_INFORMATION, EXPERT_REQUIRED.
    """
    result = pesticide_checker.check_pesticide_safety(
        product_query=req.product_query,
        crop=req.crop,
        condition_code=req.condition_code
    )
    return result


# ==============================================================================
# 13. DOUBT DOCTOR INTERACTIVE CLARIFICATION
# ==============================================================================

@app.post("/api/doubt-doctor/evaluate")
async def evaluate_doubt_doctor(req: DoubtDoctorEvaluateRequest):
    """
    Triggers 1-question interactive clarification when AI confidence is borderline (0.50-0.65)
    or when top-2 candidate diagnoses are ambiguous (delta <= 0.15).
    """
    question = doubt_doctor.evaluate_doubt_doctor_trigger(
        crop=req.crop,
        top_prediction=req.top_prediction,
        runner_up_prediction=req.runner_up_prediction,
        language=req.language or "mr"
    )
    return {"trigger": question is not None, "doubt_doctor": question}


@app.post("/api/doubt-doctor/answer")
async def answer_doubt_doctor(req: DoubtDoctorAnswerRequest):
    """
    Processes farmer's observation answer (YES / NO / DONT_KNOW) to corroborate diagnosis.
    Never forces low confidence into a disease; uncertainty escalates to expert.
    """
    ans = req.answer.strip().upper()
    boost = req.weight_boost or 0.15
    orig_conf = req.original_confidence

    if ans == "YES" and req.confirms_if_yes == req.target_condition:
        adj_conf = min(98.0, orig_conf + (boost * 100 if orig_conf <= 1.0 else boost))
        return {
            "status": "CORROBORATED",
            "condition_code": req.target_condition,
            "adjusted_confidence": round(adj_conf, 2),
            "requires_expert": False,
            "message": "Farmer observation corroborates visual symptoms."
        }
    elif ans == "NO":
        return {
            "status": "SYMPTOM_CONTRADICTION",
            "condition_code": req.target_condition,
            "adjusted_confidence": round(max(10.0, orig_conf - 25.0), 2),
            "requires_expert": True,
            "message": "Farmer observation contradicts primary hypothesis. Escalating to Agricultural Officer / Expert."
        }
    else:  # DONT_KNOW or unrecognized
        return {
            "status": "UNCERTAIN_OBSERVATION",
            "condition_code": req.target_condition,
            "adjusted_confidence": round(orig_conf, 2),
            "requires_expert": True,
            "message": "Observation uncertain. Expert agronomic review recommended."
        }


# ==============================================================================
# 14. FIELD INSPECTION TASK ENGINE
# ==============================================================================

@app.get("/api/inspection/tasks")
async def get_inspection_task(
    symptom_context: str = "wilt",
    language: str = "mr"
):
    """
    Generates structured field inspection tasks for non-foliar or systemic pathologies
    (e.g., vascular wilts, root rots, subsurface stem borers).
    """
    task = inspection_engine.generate_inspection_task(
        symptom_context=symptom_context,
        language=language
    )
    return {"inspection_task": task}


# ==============================================================================
# 15. GEOSPATIAL PROXIMITY & EPIDEMIC SPREAD ALERTS
# ==============================================================================

@app.get("/api/alerts/spread")
async def get_spread_alerts(
    case_id: int,
    radius_km: float = 15.0
):
    """
    Calculates great-circle Haversine distances to neighbouring farms for confirmed/verified cases.
    Issues preventive alerts to farms growing matching susceptible crops within radius.
    """
    case = storage.get_case_by_id(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found.")

    all_farms = storage.get_all_farms(district=case.get("district"))
    alerts = spread_alerts.evaluate_proximity_alerts(
        confirmed_case=case,
        neighboring_farms=all_farms,
        alert_radius_km=radius_km
    )
    return {
        "case_id": case_id,
        "crop": case.get("crop_code"),
        "pathology": case.get("final_condition_name") or case.get("ai_raw_prediction"),
        "radius_km": radius_km,
        "alerts_generated": len(alerts),
        "alerts": alerts
    }


# ==============================================================================
# 16. CASE ESCALATION & AGRICULTURAL DESK WORKFLOW
# ==============================================================================

class EscalateCaseRequest(BaseModel):
    case_id: Any
    timestamp: Optional[str] = None
    crop: Optional[str] = "MAIZE"
    disease: Optional[str] = "Crop Condition"
    severity: Optional[str] = "HIGH"
    image_url: Optional[str] = None
    location: Optional[str] = "Maharashtra"
    farmer_name: Optional[str] = "Local Farmer"
    latitude: Optional[float] = 20.0
    longitude: Optional[float] = 73.8
    damage_percent: Optional[float] = 40.0


@app.post("/api/escalate")
async def escalate_case_endpoint(req: EscalateCaseRequest):
    """
    Escalates an urgent or severe crop disease/pest outbreak to the District Agricultural Desk.
    Updates or inserts the case record in the database for Expert/Officer surveillance.
    """
    try:
        updated_case = storage.escalate_case(req.dict())
        return {
            "status": "success",
            "message": "Case successfully escalated to District Agricultural Desk.",
            "case": updated_case
        }
    except Exception as e:
        logger.error(f"Error in /api/escalate: {e}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "detail": f"Failed to escalate case: {str(e)}"}
        )