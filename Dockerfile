FROM python:3.10

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
WORKDIR /app

EXPOSE 8000
CMD [ "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000" ]
