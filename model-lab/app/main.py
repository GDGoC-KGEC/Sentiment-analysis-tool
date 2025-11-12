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

# path to the model
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models"/ "onxx_models" / "emotion-ferplus-8.onnx"

ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

@app.post("/predict")
async def predict(file: UploadFile = File(...), model_option: int = Form(1)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    file_bytes = await file.read()
    try:
        image = Image.open(io.BytesIO(file_bytes))
    except (OSError, ValueError) as err:
        raise HTTPException(status_code=400, detail="Invalid or corrupted image file") from err
    emotion_model  = Model(model_path=MODEL_PATH, model_option=model_option)
    emotion, prob = emotion_model.predict(pil_image=image)
    
    return {"emotion": emotion, "probabilities": prob}