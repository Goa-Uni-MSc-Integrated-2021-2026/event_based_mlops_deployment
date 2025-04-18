import os
from celery import Celery

# Set broker and backend from environment variables with defaults
broker_url = os.environ.get("CELERY_BROKER_URL", "amqp://guest:guest@localhost:5672//")
result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

# Create Celery app
celery_app = Celery(
    "transcription_worker",
    broker=broker_url,
    backend=result_backend
)

# Optional configurations
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour max task runtime
    worker_prefetch_multiplier=1,  # One task per worker at a time
    worker_max_tasks_per_child=10,  # Restart worker after 10 tasks
    broker_connection_retry_on_startup=True,
)