import os
import time
from celery import Celery
from celery.utils.log import get_task_logger

rabbit_user: str = os.environ.get("RABBITMQ_DEFAULT_USER")
rabbit_pass: str = os.environ.get("RABBITMQ_DEFAULT_PASS")

mongo_user: str = os.environ.get("MONGO_USER", "")
mongo_pass: str = os.environ.get("MONGO_PASS", "")
mongo_uri: str = f"{mongo_user}:{mongo_pass}@" if len(mongo_user) > 0 and len(mongo_pass) > 0 else ""


logger = get_task_logger(__name__)
app = Celery(
    "tasks", 
    broker=f"amqp://{rabbit_user}:{rabbit_pass}@rabbit:5672", 
    backend=f"redis://redis:6379"
)

@app.task
def add(sleep_time: int | float, x: int | float, y: int | float) -> int | float:
    logger.info('Got Request - Starting work ')
    time.sleep(sleep_time)
    logger.info('Work Finished ')
    return x + y

