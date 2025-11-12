from transformers import AutoFeatureExtractor, AutoModelForImageClassification
from PIL import Image
import numpy as np
import onnxruntime as ort
import onnx
from onnx import version_converter
import cv2
import torch
from .config import VIT_MODEL_NAME, EMOTION_TABLE

class Model:
    
    
    def __init__(self, model_path, model_option: int):
        self.emotion_table=EMOTION_TABLE
        if (model_option not in (1,2)):
            raise ValueError(f"model option must be 1 or 2, got {model_option}")
        self.model_option = model_option
        if (self.model_option==1):
            self.extractor = AutoFeatureExtractor.from_pretrained(VIT_MODEL_NAME)
            self.model = AutoModelForImageClassification.from_pretrained(VIT_MODEL_NAME)
            
        if (self.model_option == 2):            
            self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            if self.face_cascade.empty():
                raise RuntimeError("Failed to load haarcascade_frontalface_default.xml")

            self.net=cv2.dnn.readNetFromONNX(model_path)
    
    def detect_face(self, pil_image):
        image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(60, 60)
        )

        if len(faces) == 0:
            return gray  

        x,y,w,h = max(faces, key=lambda r: r[2] * r[3])
        face = gray[y:y+h, x:x+w]
        
        return face
              
    def preprocess(self, pil_image):
        gray_face = self.detect_face(pil_image=pil_image)
        resized_face = cv2.resize(gray_face, (64, 64))
        processed_face = resized_face.astype(np.float32)
        processed_face = processed_face.reshape(1,1,64,64)
        
        return processed_face
    
    def predict(self, pil_image: Image.Image):
        if (self.model_option == 1):
            inputs = self.extractor(images=pil_image, return_tensors="pt")
            with torch.no_grad():
                logits = self.model(**inputs).logits
                predicted = logits.argmax(-1).item()
            label = self.model.config.id2label[predicted]
            return label, {}

        elif (self.model_option == 2):
            processed_face = self.preprocess(pil_image=pil_image)

            self.net.setInput(processed_face)
            Output = self.net.forward()
            
            # calculatiing probabilities using softmax function                
            expanded = np.exp(Output[0] - np.max(Output[0]))
            probablities =  expanded / expanded.sum()

            prob = np.squeeze(probablities)
            prob_precentages={}
            for emotion, idx in sorted(self.emotion_table.items(), key=lambda x: x[1]):
                prob_precentages[emotion] = float(prob[idx]*100)
                
            key = [k for k, v in self.emotion_table.items() if v == prob.argmax()][0]
            label = key
            return label, prob_precentages