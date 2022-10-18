FROM python:3.10

COPY worker.requirements.txt requirements.txt
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt
WORKDIR /app
COPY tasks.py tasks.py

CMD [ "celery", "-A", "tasks", "worker", "flower", "--loglevel=INFO" ]
