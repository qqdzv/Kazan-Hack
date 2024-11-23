FROM python:3.11

RUN apt-get update && apt-get install -y \
    libgl1 \
    tesseract-ocr \
    tesseract-ocr-rus \
    tesseract-ocr-eng \
    libtesseract-dev \
    libleptonica-dev && \
    apt-get clean

WORKDIR /app

# Устанавливаем зависимости
RUN pip install --upgrade pip
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# Устанавливаем рабочую директорию
COPY . /app

# Копируем файлы проекта в контейнер
COPY . .