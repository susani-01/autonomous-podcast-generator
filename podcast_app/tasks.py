from podcast_app.audio_mixer import mix_podcast
from podcast_app.tts_engine import synthesize_script
from podcast_app.script_generator import generate_script, fetch_article
from celery import Celery
from dotenv import load_dotenv
import os
import uuid

os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

load_dotenv()

celery_app = Celery(
    "podcast_tasks",
    broker=os.getenv("redis_url", "redis://redis:6379/0"),
    backend=os.getenv("redis", "redis://redis:6379/0"),
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_track_started=True,
    result_expires=3600,
)


@celery_app.task(bind=True, name="generate_podcast")
def generate_podcast(self, input_text: str = None, url: str = None, music: bool = True):
    job_id = str(uuid.uuid4())[:8]
    try:
        self.update_state(
            state="PROGRESS",
            meta={
                "step": 1,
                "total_steps": 4,
                "message": "Fetching article...",
                "job_id": job_id,
            },
        )

        if url:
            article_text = fetch_article(url)
        elif input_text:
            article_text = input_text
        else:
            raise ValueError("Either url or input_text must be provided")

        self.update_state(
            state="PROGRESS",
            meta={
                "step": 2,
                "total_steps": 4,
                "message": "Generating podcast script with GPT-4...",
                "job_id": job_id,
            },
        )
        script = generate_script(article_text)

        self.update_state(
            state="PROGRESS",
            meta={
                "step": 3,
                "total_steps": 4,
                "message": f"Synthesizing {len(script)} dialogue lines...",
                "job_id": job_id,
            },
        )

        audio_paths = synthesize_script(script, job_id=job_id)

        self.update_state(
            state="PROGRESS",
            meta={
                "step": 4,
                "total_steps": 4,
                "message": "Mixing audio and background music...",
                "job_id": job_id,
            },
        )

        music_path = "podcast_app/music/background.mp3" if music else None

        podcast_path = mix_podcast(
            audio_paths=audio_paths, script=script, job_id=job_id, music_path=music_path
        )

        return {
            "status": "SUCCESS",
            "job_id": job_id,
            "podcast_path": podcast_path,
            "script": script,
            "total_lines": len(script),
        }
    except Exception as e:
        self.update_state(state="FAILURE", meta={
                          "message": str(e), "job_id": job_id})
        raise
