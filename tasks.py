import os
import time
from celery import Celery
from celery.utils.log import get_task_logger

rabbit_user: str = os.environ.get('RABBITMQ_DEFAULT_USER')
rabbit_pass: str = os.environ.get('RABBITMQ_DEFAULT_PASS')

logger = get_task_logger(__name__)
app = Celery(
    'tasks', 
    broker=f'amqp://{rabbit_user}:{rabbit_pass}@rabbit:5672/0', 
    backend='redis://redis:6379'
)

@app.task
def add(x, y):
    logger.info('Got Request - Starting work ')
    time.sleep(5)
    logger.info('Work Finished ')
    return x + y