FROM python:3.11

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    tesseract-ocr \
    tesseract-ocr-rus \
    tesseract-ocr-eng \
    libtesseract-dev \
    libleptonica-dev && \
    apt-get clean

WORKDIR /app

# Clear pip cache and install dependencies
RUN pip cache purge

# Install pip dependencies from requirements.txt
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt -c constraints.txt

# Copy project files
COPY . .

# Set the working directory in the container
WORKDIR /app