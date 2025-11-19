from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image
import io
import os
import logging

from app.model import Model

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Face Sentiment API")

# ✅ Path to the model (fixed typo: onxx_models → onnx_models)
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "onnx_models" / "emotion-ferplus-8.onnx"
if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")

# ✅ Validate CORS origins properly
ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000").split(",")
if not ALLOWED_ORIGINS or ALLOWED_ORIGINS == [""]:
    raise RuntimeError("No allowed origins configured in CORS_ALLOWED_ORIGINS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

# ✅ Pre-load both model options at startup to avoid race conditions
emotion_models = {
    1: Model(model_path=MODEL_PATH, model_option=1),  # HuggingFace ViT
    2: Model(model_path=MODEL_PATH, model_option=2)   # ONNX with CV2
}

# ✅ Prediction endpoint with corrected error handling
@app.post("/predict")
async def predict(file: UploadFile = File(...), model_option: int = Form(1)):
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Read file bytes
    file_bytes = await file.read()
    try:
        image = Image.open(io.BytesIO(file_bytes))
    except (OSError, ValueError) as err:
        raise HTTPException(status_code=400, detail="Invalid or corrupted image file") from err

    try:
        # Validate model option
        model = emotion_models.get(model_option)
        if not model:
            raise HTTPException(status_code=400, detail="Invalid model option")

        # Run prediction
        prediction = model.predict(image)
        return {"prediction": prediction}

    except HTTPException:
        # Preserve explicit HTTP errors
        raise
    except Exception as e:
        # Log internal error for debugging
        logger.exception("Unexpected error during prediction")
        # Return generic message to client
        raise HTTPException(status_code=500, detail="Internal server error")
