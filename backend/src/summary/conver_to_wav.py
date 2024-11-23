# from pydub import AudioSegment
# import os


# def convert_to_wav(input_file, output_file):
#     """
#     Конвертирует mp3 или mp4 файл в wav формат.

#     Args:
#         input_file (str): Путь к входному mp3 или mp4 файлу
#         output_file (str): Путь к выходному wav файлу

#     Returns:
#         bool: True, если конвертация прошла успешно, False в противном случае
#     """

#     file_extension = os.path.splitext(input_file)[1].lower()

#     if file_extension == '.mp3':
#         audio = AudioSegment.from_mp3(input_file)
#     elif file_extension == '.mp4':
#         audio = AudioSegment.from_mp4(input_file)
#     else:
#         print("Неподдерживаемый формат аудио файла.")
#         return False

#     # Сохраняем в wav формат
#     audio.export(output_file, format="wav")

#     return True

