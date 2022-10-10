FROM python:3.10

RUN pip install fastapi uvicorn
WORKDIR /app

EXPOSE 8000
CMD [ "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000" ]
