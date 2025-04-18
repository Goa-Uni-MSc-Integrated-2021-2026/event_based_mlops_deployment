from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime

class ModelSize(str, Enum):
    TINY = "tiny"
    BASE = "base"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

class TaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class TranscriptionRequest(BaseModel):
    model_size: ModelSize = Field(default=ModelSize.BASE, description="Whisper model size to use")

class TranscriptionResponse(BaseModel):
    task_id: str
    message: str
    created_at: datetime = Field(default_factory=datetime.now)

class TranscriptionResult(BaseModel):
    task_id: str
    status: TaskStatus
    result: Optional[str] = None
    error: Optional[str] = None
    completed_at: Optional[datetime] = None

class TaskStatusResponse(BaseModel):
    task_id: str
    status: TaskStatus
    created_at: datetime
    model_size: ModelSize