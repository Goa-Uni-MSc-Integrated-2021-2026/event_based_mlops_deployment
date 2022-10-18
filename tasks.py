import os
import time
from celery import Celery
from celery.utils.log import get_task_logger

rabbit_user: str = os.environ.get("RABBITMQ_DEFAULT_USER")
rabbit_pass: str = os.environ.get("RABBITMQ_DEFAULT_PASS")

mongodb_user: str = ""
mongodb_pass: str = ""
mongodb_uri: str = f"{mongodb_user}:{mongodb_pass}@" if len(mongodb_user) > 0 and len(mongodb_pass) > 0 else ""


logger = get_task_logger(__name__)
app = Celery(
    "tasks", 
    broker=f"amqp://{rabbit_user}:{rabbit_pass}@rabbit:5672", 
    backend=f"mongodb://{mongodb_uri}mongo:27017"
)

@app.task
def add(x: int | float, y: int | float) -> int | float:
    logger.info('Got Request - Starting work ')
    time.sleep(5)
    logger.info('Work Finished ')
    return x + y

