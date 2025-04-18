import os
import uuid
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException, Form, Depends, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
from typing import Optional, List
from celery_worker.tasks import transcribe_audio
from celery.result import AsyncResult
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get default model size from environment
DEFAULT_MODEL_SIZE = os.environ.get("DEFAULT_MODEL_SIZE", "base")
FORCE_BASE_MODEL = os.environ.get("WHISPER_MODEL") == "base"

app = FastAPI(
    title="Audio Transcription API",
    description="API for transcribing audio files using OpenAI's Whisper model",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure audio directory exists
AUDIO_DIR = Path("audio_data")
AUDIO_DIR.mkdir(exist_ok=True)

class TranscriptionResponse(BaseModel):
    task_id: str
    message: str

class TranscriptionResult(BaseModel):
    task_id: str
    status: str
    result: Optional[str] = None
    error: Optional[str] = None
    model_used: str = "base"

@app.post("/transcribe/", response_model=TranscriptionResponse, tags=["Transcription"])
async def create_transcription(
    file: UploadFile = File(...),
    model_size: str = Form("base", description="Whisper model size (only base is currently supported)")
):
    """
    Upload an audio file for transcription.
    
    - **file**: Audio file to transcribe (mp3, wav, m4a, etc.)
    - **model_size**: Whisper model size to use
    """
    # Force base model if configured
    if FORCE_BASE_MODEL:
        model_size = "base"
    
    # Validate file type
    valid_extensions = [".mp3", ".wav", ".m4a", ".flac", ".ogg"]
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in valid_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format. Supported formats: {', '.join(valid_extensions)}"
        )
    
    # Generate unique filename for the audio
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = AUDIO_DIR / unique_filename
    
    # Save uploaded file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logger.info(f"File saved: {file_path}")
    except Exception as e:
        logger.error(f"Error saving file: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to save uploaded file")
    
    # Start transcription task
    try:
        # Always use base model
        task = transcribe_audio.delay(str(file_path), "base")
        logger.info(f"Task created: {task.id}")
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to start transcription task")
    
    return TranscriptionResponse(
        task_id=task.id,
        message=f"Transcription task started successfully using base model"
    )

@app.get("/transcription/{task_id}", response_model=TranscriptionResult, tags=["Transcription"])
async def get_transcription_result(task_id: str):
    """
    Get the result of a transcription task.
    
    - **task_id**: ID of the transcription task
    """
    try:
        task = AsyncResult(task_id)
        
        if task.state == 'PENDING':
            return TranscriptionResult(
                task_id=task_id,
                status="pending",
                result=None,
                error=None,
                model_used="base"
            )
        elif task.state == 'STARTED':
            return TranscriptionResult(
                task_id=task_id,
                status="processing",
                result=None,
                error=None,
                model_used="base"
            )
        elif task.state == 'FAILURE':
            return TranscriptionResult(
                task_id=task_id,
                status="failed",
                result=None,
                error=str(task.info),
                model_used="base"
            )
        else:
            return TranscriptionResult(
                task_id=task_id,
                status="completed",
                result=task.result,
                error=None,
                model_used="base"
            )
    except Exception as e:
        logger.error(f"Error checking task status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to check task status")

@app.get("/health", tags=["System"])
async def health_check():
    """
    Health check endpoint for the API.
    """
    return {
        "status": "healthy", 
        "version": "1.0.0",
        "model": "base",
        "configuration": {
            "force_base_model": FORCE_BASE_MODEL,
            "default_model": DEFAULT_MODEL_SIZE
        }
    }

@app.get("/", tags=["System"])
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "name": "Audio Transcription API",
        "version": "1.0.0",
        "model": "base",
        "endpoints": {
            "transcribe": "/transcribe/",
            "transcription_result": "/transcription/{task_id}",
            "health": "/health"
        },
        "documentation": "/docs"
    }