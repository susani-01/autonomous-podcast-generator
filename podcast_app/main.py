from fastapi import FastAPI,BackgroundTasks,HTTPException
from fastapi.responses import FileResponse,JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Optional
import os

load_dotenv()
from podcast_app.tasks import generate_podcast,celery_app

app = FastAPI(
    title="AI podcast Generator",
    description="Turns any article into fully mixed AI podcast with two hosts",
    version="1.0.0"
)

class ArticleRequest(BaseModel):
    text:Optional[str] = None
    url:Optional[str]=None
    music:bool = True

    class Config:
        json_schema_extra={
            "example":{
                "text":"Enter your article here",
                "music": True
            }
        }

@app.get("/")
def root():
    return{
        "message":"AI Podcast Generator",
        "endpoints":{
            "POST /generate": "Submit article to generate podcast",
            "GET /status/{task_id}": "Check generation progress",
            "GET /download/{task_id}": "Download finished podcast mp3",
            "GET /script/{task_id}": "Get the generated script"
        }
    }

@app.post("/generate")
def generate(request: ArticleRequest):
    if not request.text and not request.url:
        raise HTTPException(
            status_code=400,
            detail="Provide either 'text' or 'url'"
        )

    task = generate_podcast.delay(
        input_text=request.text,
        url=request.url,
        music=request.music
    )
    return JSONResponse({
        "task_id":task.id,
        "status":"PENDING",
        "message":"Podcast generation started",
        "check_status":f"/status/{task.id}"
    })

@app.get("/status/{task_id}")
def get_status(task_id:str):
    task=celery_app.AsyncResult(task_id)

    if task.state == "PENDING":
        return {"task_id":task_id,"status":"PENDING","message":"Waiting to start..."}

    elif task.state == "PROGRESS":
        meta = task.info or {}
        return {
            "task_id": task_id,
            "status": "PROGRESS",
            "step": meta.get("step"),
            "total_steps": meta.get("total_steps"),
            "message": meta.get("message"),
            "job_id": meta.get("job_id")
        }
    elif task.state == "SUCCESS":
        result=task.result
        return {
            "task_id":task_id,
            "status":"SUCCESS",
            "job_id":result["job_id"],
            "total_lines":result["total_lines"],
            "download":f"/download/{task_id}",
            "script":f"/script/{task_id}"
        }
    elif task.state == "FAILURE":
        return {
            "task_id":task_id,
            "status":"FAILURE",
            "error":str(task.info)
        }
@app.get("/download/{task_id}")
def download_podcast(task_id: str):
    task = celery_app.AsyncResult(task_id)

    if task.state != "SUCCESS":
        raise HTTPException(
            status_code=400,
            detail=f"Podcast not ready yet. Status: {task.state}"
        )
    podcast_path=task.result["podcast_path"]

    if not os.path.exists(podcast_path):
        raise HTTPException(status_code=404,detail="Podcast file not found")

    return FileResponse(
        podcast_path,
        media_type="audio/mpeg",
        filename=f"podcast_{task.result['job_id']}.mp3"
    )

@app.get("/script/{task_id}")
def get_script(task_id: str):
    task = celery_app.AsyncResult(task_id)

    if task.state != "SUCCESS":
        raise HTTPException(
            status_code=400,
            detail=f"Podcast not ready yet.Status: {task.state}"
        )
    return {
        "task_id":task_id,
        "script":task.result["script"]
    }

@app.get("/health")
def health():
    return {
        "status":"healthy",
        "redis":"connected",
        "version":"1.0.0"
    }
