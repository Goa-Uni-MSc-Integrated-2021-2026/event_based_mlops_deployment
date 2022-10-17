FROM python:3.10

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
WORKDIR /app

CMD [ "celery", "-A", "tasks", "worker", "--loglevel=INFO" ]
