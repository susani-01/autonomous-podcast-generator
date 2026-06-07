````markdown
#  Autonomous Podcast Generator

An end-to-end AI system that automatically transforms a topic or article into a fully narrated podcast episode. The platform leverages Large Language Models (LLMs), Text-to-Speech (TTS), and an automated audio processing pipeline to generate production-ready podcasts with minimal human intervention.

---

##  Features

-  **AI Script Generation**
  - Generates structured podcast scripts from a topic or article.
  - Supports multi-speaker dialogue generation.

-  **Neural Text-to-Speech**
  - Uses Kokoro TTS to convert generated scripts into natural-sounding speech.
  - Supports multiple voices for creating conversational podcast experiences.

-  **Automatic Audio Mixing**
  - Combines individual voice tracks.
  - Supports optional background music integration.
  - Exports a final MP3 podcast.

-  **Asynchronous Processing**
  - Uses Celery workers and Redis for long-running AI tasks.
  - Allows podcast generation jobs to run in the background.

-  **REST API**
  - Built with FastAPI for easy integration with web or mobile applications.
  - Automatic API documentation via Swagger UI.

-  **Containerized Deployment**
  - Docker and Docker Compose support for reproducible environments.

---

##  System Architecture

```text
                 +----------------------+
                 |     User Request     |
                 | (Topic or Article)   |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 |   FastAPI Backend    |
                 |    REST API Layer    |
                 +----------+-----------+
                            |
                     Creates Job
                            |
                            v
                 +----------------------+
                 |        Redis         |
                 |    Message Broker    |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 |    Celery Worker     |
                 | Async Task Execution |
                 +----------+-----------+
                            |
           +----------------+----------------+
           |                                 |
           v                                 v
+----------------------+       +----------------------+
|   LLM Script Engine  |       |     Kokoro TTS      |
|  (Podcast Dialogue)  |       |  Neural Voice Synth |
+----------------------+       +----------------------+
           |                                 |
           +----------------+----------------+
                            |
                            v
                 +----------------------+
                 |  Pydub + FFmpeg      |
                 |    Audio Mixing      |
                 +----------+-----------+
                            |
                            v
                 +----------------------+
                 |   Final Podcast      |
                 |      MP3 Output      |
                 +----------------------+
```

---

##  Technology Stack

| Category | Technologies |
|----------|-------------|
| Backend | Python, FastAPI |
| Task Queue | Celery |
| Message Broker | Redis |
| AI | Large Language Models (OpenAI GPT) |
| Speech Synthesis | Kokoro TTS |
| Audio Processing | Pydub, FFmpeg |
| Containerization | Docker, Docker Compose |
| Testing | Pytest |
| CI/CD | GitHub Actions |

## 📁 Project Structure

```text
autonomous-podcast-generator/
│
├── podcast_app/
│   ├── main.py
│   ├── tasks.py
│   ├── script_generator.py
│   ├── tts_engine.py
│   ├── audio_mixer.py
│   ├── outputs/
│   └── music/
│
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---


## 🐳 Running with Docker

```bash
docker compose up --build
```

The application starts:

- FastAPI API
- Redis server
- Celery worker

---


##  Example Workflow

1. User submits a topic.
2. The API creates a generation job.
3. Celery processes the request asynchronously.
4. The LLM generates a podcast script.
5. The TTS engine synthesizes speech.
6. The audio mixer combines tracks.
7. A final MP3 podcast is exported.

---

##  Testing

Run unit tests:

```bash
pytest
```

Run linting:

```bash
flake8 .
```

---

##  Motivation

Podcast creation typically requires multiple manual steps, including script writing, voice recording, and audio editing. This project explores how modern AI systems can automate the entire pipeline, reducing production time while maintaining high-quality output.

The project also serves as a practical demonstration of integrating modern AI workflows with scalable backend engineering practices such as asynchronous task queues, containerization, and automated testing.

---

## Future Improvements

- Multi-language podcast generation
- Voice cloning support
- Web frontend for podcast management
- Streaming audio generation
- Cloud deployment (AWS/GCP/Azure)
- Multi-agent podcast planning pipeline

---

````

