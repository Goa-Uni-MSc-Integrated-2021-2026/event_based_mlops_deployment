FROM python:3.11.11

COPY app.requirements.txt requirements.txt
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt
WORKDIR /app
COPY app.py app.py

EXPOSE 8000
CMD [ "uvicorn", "app:app", "--reload", "--host", "0.0.0.0", "--port", "8000" ]
