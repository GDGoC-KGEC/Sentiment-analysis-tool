from fastapi import FastAPI, File, UploadFile
from contextlib import asynccontextmanager
from PIL import Image
import io
from app.model import predict_emotion, load_model, is_model_ready

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_model()
    yield

app = FastAPI(title="Face Sentiment API", lifespan=lifespan)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read()))
    emotion = predict_emotion(image)
    return {"emotion": emotion}

@app.get("/health")
def get_health():
    if is_model_ready():
        return {"status" : "ok"}
    else:
        return {"status" : "unavailable"}
