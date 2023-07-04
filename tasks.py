import os
import time
from celery import Celery
from celery.utils.log import get_task_logger

RABBIT_USER: str = os.environ.get("RABBITMQ_DEFAULT_USER")
RABBIT_PASS: str = os.environ.get("RABBITMQ_DEFAULT_PASS")
RABBIT_HOST: str = os.environ.get("RABBITMQ_DEFAULT_HOST")
RABBIT_PORT: int = int(os.environ.get("RABBITMQ_DEFAULT_PORT"))

REDIS_HOST: str = os.environ.get("REDIS_HOST")
REDIS_PORT: int = int(os.environ.get("REDIS_PORT"))

logger = get_task_logger(__name__)
app = Celery(
    "tasks",
    broker=f"amqp://{RABBIT_USER}:{RABBIT_PASS}@{RABBIT_HOST}:{RABBIT_PORT}",
    backend=f"redis://{REDIS_HOST}:{REDIS_PORT}",
)


@app.task
def add(sleep_time: int | float, x: int | float, y: int | float) -> int | float:
    logger.info("Got Request - Starting work ")
    time.sleep(sleep_time)
    logger.info("Work Finished ")
    return x + y
