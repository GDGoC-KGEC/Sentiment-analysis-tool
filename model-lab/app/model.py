from transformers import AutoFeatureExtractor, AutoModelForImageClassification
from PIL import Image
import numpy as np
import onnxruntime as ort
import onnx
from onnx import version_converter
import cv2
import torch

class Model:
    #emotion table for Emotion-ferplus
    emotion_table = {'neutral':0, 'happiness':1, 'surprise':2, 'sadness':3, 'anger':4, 'disgust':5, 'fear':6, 'contempt':7}
    
    
    VIT_MODEL_NAME = "trpakov/vit-face-expression"

    extractor = AutoFeatureExtractor.from_pretrained(VIT_MODEL_NAME)
    model = AutoModelForImageClassification.from_pretrained(VIT_MODEL_NAME)
    
    def __init__(self, model_path, model_option: int):
        self.model_option = model_option
        if (model_option == 2):
            # To be used if model conversion is needed in future versions
            # model = onnx.load(model_path)
            # converted_model = version_converter.convert_version(model, 12)
            # converted_path = model_path.replace("-8.onnx", "-12.onnx")
            # onnx.save_model(converted_model, converted_path)
            
            # self.session = ort.InferenceSession(model_path)
            self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            
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
        
        # Extra padding around detected face (not required for now)
        # padding = int(0.2 * max(w, h))  # Increased from 10% to 20%
        # x = max(0, x - padding)
        # y = max(0, y - padding)
        # w = min(gray.shape[1] - x, w + 2 * padding)
        # h = min(gray.shape[0] - y, h + 2 * padding)
        
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