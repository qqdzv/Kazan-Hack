import aiohttp
import json
import asyncio
import pytesseract
from PIL import Image
import os
from pdf2image import convert_from_path
from src.config import CHAT_BOT_API
import asyncio

def process_image(img_path: str) -> Image:
    # Get the file extension
    file_extension = os.path.splitext(img_path)[1].lower()

    # If the file is a PDF, convert to an image
    if file_extension == '.pdf':
        images = convert_from_path(img_path, first_page=1, last_page=1)  # Only first page
        return images[0]  # Return the first page as an image

    # If it's a JPG or PNG, open the image
    elif file_extension in ['.jpg', '.jpeg', '.png']:
        return Image.open(img_path)

    else:
        raise ValueError("Unsupported file format. Only PDF, JPG, and PNG are supported.")


async def process_image_to_json(img: str) -> dict:
    url = "https://api.aimlapi.com/chat/completions"
    img = process_image(img)

    # Extract text from the image using Tesseract
    text = await asyncio.to_thread(pytesseract.image_to_string, img, lang="rus")
    headers = {
        "Authorization": f"Bearer {CHAT_BOT_API}",
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "model": "gpt-4o",  # исправлен идентификатор модели
        "response_format": {"type": "json_object"},

        "messages": [
            {
                "role": "system",
                "content": """
                    Ты получаешь на вход текст с результатами медицинских исследований. Приведи текст в порядок.
                    Убери из текста персональные данные пациента (имя, дату рождения, пол, адрес) и врача (ФИО, контактные данные).
                    Выдели из текста тип осмотра или исследования, если он указан, и добавь в переменную type_analysis. Если тип осмотра не указан, пойми по тексту что это за исследование или прием у врача.
                    Выдели из текста дату выполнения осмотра или исследования и добавь её в переменную data. 
                    Весь остальной текст добавь в переменную text. Отдай результат в формате JSON в виде:
                    {"type_analysis": type_analysis, "data": data, "text": text}
                    Обязательно закрывай все скобки и кавычки, иначе ответ не будет принят.
                """
            },
            {
                "role": "user",
                "content": text,
            }
        ]
    })


    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=payload) as response:
            response_data = await response.json()
            data = (response_data['choices'][0]['message']['content'] + '"}')
            data_dict = json.loads(data)
            return data_dict


