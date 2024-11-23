import cv2
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification
import base64
import numpy as np

def get_eye_answer(image_base64: str):
    
    if image_base64.startswith("data:image/jpeg;base64,"):
        image_base64 = image_base64.split(",")[1]
    if image_base64.startswith("data:image/png;base64,"):
        image_base64 = image_base64.split(",")[1]

    processor = AutoImageProcessor.from_pretrained(
        "SM200203102097/eyeDiseasesDetectionModel"
    )
    eye_model = AutoModelForImageClassification.from_pretrained(
        "SM200203102097/eyeDiseasesDetectionModel"
    )
    
    im_bytes = base64.b64decode(image_base64)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
    image = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

    disease_eye_translation = {
        "AMD": "Возрастная макулярная дегенерация",
        "Cataract": "Катаракта",
        "Diabetes": "Диабет",
        "Glaucoma": "Глаукома",
        "Hypertension": "Гипертония",
        "Myopia": "Близорукость",
        "Normal": "Норма",
        "Other": "Другое",
    }

    inputs = processor(image, return_tensors="pt")

    with torch.no_grad():
        logits = eye_model(**inputs).logits

    predicted_label = logits.argmax(-1).item()
    return (disease_eye_translation[eye_model.config.id2label[predicted_label]])
