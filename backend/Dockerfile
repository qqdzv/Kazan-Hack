FROM python:3.11

# Установка необходимых системных зависимостей
RUN apt-get update && apt-get install -y \
    libgl1 \
    tesseract-ocr \
    tesseract-ocr-rus \
    tesseract-ocr-eng \
    libtesseract-dev \
    libleptonica-dev && \
    apt-get clean

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY ./requirements.txt ./requirements.txt
COPY requirements.txt constraints.txt ./


# Очищаем кеш pip перед установкой зависимостей и устанавливаем их
RUN pip cache purge && \
    pip install --upgrade pip && \
    pip install -r requirements.txt -c constraints.txt

# Копируем весь проект в контейнер
COPY . /app

