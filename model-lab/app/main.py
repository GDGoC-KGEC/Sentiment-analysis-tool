from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from PIL import Image
import io
import os
from app.model import Model
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Face Sentiment API")

# Path to the model (fixed typo: onxx_models → onnx_models)
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "onnx_models" / "emotion-ferplus-8.onnx"
if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")

# Validate CORS origins properly
ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000").split(",")
if not ALLOWED_ORIGINS or ALLOWED_ORIGINS == [""]:
    raise RuntimeError("No allowed origins configured in CORS_ALLOWED_ORIGINS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

# Load model once at startup (not per request)
emotion_model = Model(model_path=MODEL_PATH, model_option=1)

@app.post("/predict")
async def predict(file: UploadFile = File(...), model_option: int = Form(1)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    file_bytes = await file.read()
    try:
        image = Image.open(io.BytesIO(file_bytes))
    except (OSError, ValueError) as err:
        raise HTTPException(status_code=400, detail="Invalid or corrupted image file") from err

    try:
        # Use already loaded model, but allow overriding option if needed
        emotion_model.model_option = model_option
        emotion, prob = emotion_model.predict(pil_image=image)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model inference failed: {e}") from e

    return {"emotion": emotion, "probabilities": prob}
