from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import JSONResponse
import uuid, os

from models.whisper import transcribe_audio

router = APIRouter()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/task")
async def create_task(request: Request, file: UploadFile = File(...)):
    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    task = transcribe_audio.delay(file_path)

    return JSONResponse(
        {
            "message": "Transcription started",
            "task_id": task.id
        },
        status_code=202
    )
