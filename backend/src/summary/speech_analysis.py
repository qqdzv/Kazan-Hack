# from speechkit import configure_credentials, creds
# from conver_to_wav import convert_to_wav
# import os
# from speechkit import model_repository
# from speechkit.stt import AudioProcessingType
# import aiohttp
# import json
# import asyncio

# configure_credentials(
#     yandex_credentials=creds.YandexCredentials(
#         api_key='AQVN2Fkj0H49svrLqatMpAeAvp6_bWCdnVxuduuT'
#     )
# )


# def check_wav_extension(file_path):
#     _, extension = os.path.splitext(file_path)  # Получаем кортеж (имя_файла, расширение)
#     return extension.lower() == '.wav'


# def speech(file_path: str):
#     if not check_wav_extension(file_path):
#         convert_to_wav(file_path, file_path)

#     model = model_repository.recognition_model()

#     model.model = 'general'
#     model.language = 'ru-RU'
#     model.audio_processing_type = AudioProcessingType.Full

#     result = model.transcribe_file(file_path)
#     normalized_text = ""

#     # Write the first result to the file and save it in the variable
#     with open('transcription_result.txt', 'w', encoding='utf-8') as f:
#         for c, res in enumerate(result):
#             if c == 0:
#                 normalized_text = res.normalized_text  # Save the normalized text
#                 f.write(f'{normalized_text}\n')  # Write it to the file

#     # Return the normalized text
#     return normalized_text


# async def process_speech_to_report(file_path: str) -> dict:
#     url = "https://api.aimlapi.com/chat/completions"
#     text = speech(file_path)
#     headers = {
#         "Authorization": "Bearer ad1eccff91204ca38592f9550f2fecca",
#         "Content-Type": "application/json"
#     }

#     payload = json.dumps({
#         "model": "gpt-4o",  # исправлен идентификатор модели
#         "response_format": {"type": "json_object"},

#         "messages": [
#             {
#                 "role": "system",
#                 "content": """
    
#     Ты - медицинский ассистент. Проанализируй приведенный ниже текст диалога между врачом и пациентом и извлеки информацию для заполнения формы осмотра в формате JSON.
#     Важно: Обязательно включи в ответ все поля, указанные в структуре JSON, даже если информация отсутствует. Если данных нет, заполни поле пустой строкой "".
#     Пример выходного JSON:
    
#     {{
#       "дата_приёма": "",
#       "жалобы": "",
#       "анамнез": {{
#         "настоящее_заболевание": "",
#         "жизни": "",
#         "аллергологический": "",
#         "наследственность": ""
#       }},
#       "общее_состояние": "",
#       "виталные_показатели": {{
#         "температура_тела_С": "",
#         "артериальное_давление_мм_рт_ст": "",
#         "ЧСС": "",
#         "частота_дыхания": ""
#       }},
#       "диагноз": "",
#       "назначения_и_рекомендации": ""
#     }}
    
#     Верни JSON, заполнив только те поля, которые указаны в структуре JSON.
#     """
#             },
#             {
#                 "role": "user",
#                 "content": text,
#             }
#         ]
#     })

#     async with aiohttp.ClientSession() as session:
#         async with session.post(url, headers=headers, data=payload) as response:
#             response_data = await response.json()
#             data = (response_data['choices'][0]['message']['content'])
#             data_dict = json.loads(data)
#             print(data_dict)
#             return data_dict


# if __name__ == '__main__':
#     file_path = 'test.wav'
#     asyncio.run(process_speech_to_report(file_path))
