from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image
import io
import os
from app.model import predict_emotion
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="Face Sentiment API")

ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    try:
        image = Image.open(io.BytesIO(await file.read()))
    except (OSError, ValueError) as err:
        raise HTTPException(status_code=400, detail="Invalid or corrupted image file") from err
    emotion = predict_emotion(image)
    return {"emotion": emotion}