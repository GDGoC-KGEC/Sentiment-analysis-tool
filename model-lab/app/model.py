from typing import Optional
from transformers import AutoFeatureExtractor, AutoModelForImageClassification
from PIL import Image
import torch

MODEL_NAME = "trpakov/vit-face-expression"

extractor = None
model = None

def load_model():
    global extractor, model
    extractor = AutoFeatureExtractor.from_pretrained(MODEL_NAME)
    model = AutoModelForImageClassification.from_pretrained(MODEL_NAME)

def is_model_ready() -> bool:
    return extractor is not None and model is not None

def predict_emotion(image: Image.Image):
    inputs = extractor(images=image, return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits
        predicted = logits.argmax(-1).item()
    label = model.config.id2label[predicted]
    return label
