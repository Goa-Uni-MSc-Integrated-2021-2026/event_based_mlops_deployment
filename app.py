import os
from fastapi import FastAPI, Request
from celery.result import AsyncResult
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def index():
    return JSONResponse({"status": "ok"}, 200)

@app.post("/status")
def task_status(request: Request):
    try:
        data = request.json()
        if "taskID" not in data:
            return JSONResponse({"status": "specify correct json body"}, 400)
        task_id = data["taskID"]
        res = AsyncResult(task_id)
        return JSONResponse({"taskStatus": res.status}, 200)
    except Exception:
        return JSONResponse({"status": "invalid json body"}, 400)

@app.post("/task")
def create_project(request: Request):
    try:
        data = request.json()
        return JSONResponse({"status": "ok"}, 200)
    except Exception:
        return JSONResponse({"status": "invalid json body"}, 400)

@app.post("/user")
def create_user(request: Request):
    try:
        data = request.json()
        return JSONResponse({"status": "ok"}, 200)
    except Exception:
        return JSONResponse({"status": "invalid json body"}, 400)
