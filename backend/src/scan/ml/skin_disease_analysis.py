import cv2
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification
import base64
import numpy as np

def get_answer(image_base64 : str):
    
    if image_base64.startswith("data:image/jpeg;base64,"):
        image_base64 = image_base64.split(",")[1]
    if image_base64.startswith("data:image/png;base64,"):
        image_base64 = image_base64.split(",")[1]
        
    processor = AutoImageProcessor.from_pretrained("Muzmmillcoste/finetuned-dermnet")
    dermnet_model = AutoModelForImageClassification.from_pretrained(
        "Muzmmillcoste/finetuned-dermnet"
    )
    
    im_bytes = base64.b64decode(image_base64)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
    image = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

    disease_translation = {
        "Acne and Rosacea Photos": "Акне и розацеа",
        "Actinic Keratosis Basal Cell Carcinoma and other Malignant Lesions": "Актинический кератоз, базальноклеточная карцинома и другие злокачественные поражения",
        "Lupus and other Connective Tissue diseases": "Волчанка и другие заболевания соединительной ткани",
        "Melanoma Skin Cancer Nevi and Moles": "Меланома, рак кожи, невусы и родинки",
        "Nail Fungus and other Nail Disease": "Грибок ногтей и другие заболевания ногтей",
        "Poison Ivy Photos and other Contact Dermatitis": "Ядовитый плющ и другие контактные дерматиты",
        "Psoriasis pictures Lichen Planus and related diseases": "Псориаз, плоский лишай и связанные заболевания",
        "Scabies Lyme Disease and other Infestations and Bites": "Чесотка, болезнь Лайма и другие паразитарные заболевания и укусы",
        "Seborrheic Keratoses and other Benign Tumors": "Себорейный кератоз и другие доброкачественные опухоли",
        "Systemic Disease": "Системные заболевания",
        "Tinea Ringworm Candidiasis and other Fungal Infections": "Трихофития, кандидоз и другие грибковые инфекции",
        "Urticaria Hives": "Крапивница",
        "Atopic Dermatitis Photos": "Атопический дерматит",
        "Vascular Tumors": "Сосудистые опухоли",
        "Vasculitis Photos": "Васкулит",
        "Warts Molluscum and other Viral Infections": "Бородавки, контагиозный моллюск и другие вирусные инфекции",
        "Bullous Disease Photos": "Буллезные заболевания",
        "Cellulitis Impetigo and other Bacterial Infections": "Целлюлит, импетиго и другие бактериальные инфекции",
        "Eczema Photos": "Экзема",
        "Exanthems and Drug Eruptions": "Экзантемы и лекарственные высыпания",
        "Hair Loss Photos Alopecia and other Hair Diseases": "Выпадение волос, алопеция и другие заболевания волос",
        "Herpes HPV and other STDs Photos": "Герпес, ВПЧ и другие ЗППП",
        "Light Diseases and Disorders of Pigmentation": "Заболевания, связанные со светом, и нарушения пигментации",
    }


    inputs = processor(image, return_tensors="pt")

    with torch.no_grad():
        logits = dermnet_model(**inputs).logits

    # model predicts either glaucoma or non-glaucoma.
    predicted_label = logits.argmax(-1).item()
    return (disease_translation[dermnet_model.config.id2label[predicted_label]])
