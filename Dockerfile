from python:3.12-slim

Run apt-get update && apt-get install -y \
    ffmpeg \
    espeak \
    espeak-ng \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .
RUN mkdir -p podcast_app/outputs podcast_app/music

EXPOSE 8000