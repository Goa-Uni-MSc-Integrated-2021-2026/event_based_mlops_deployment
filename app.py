import os
import random
from fastapi import FastAPI, Request
from celery.result import AsyncResult
from fastapi.responses import JSONResponse
from tasks import add

app = FastAPI()

@app.get("/")
async def index():
    return JSONResponse({"status": "ok"}, 200)

@app.get("/task")
async def create_task(request: Request):
    try:
        data = await request.json()
        amount = float(data["amount"]) if "amount" in data else random.randrange(0, 10)
        x = float(data["x"]) if "x" in data else random.randint(0, 100000000)
        y = float(data["y"]) if "y" in data else random.randint(0, 100000000)
        task = add.delay(amount, x, y)
        return JSONResponse({"status": "ok", "taskId": task.id, "amount": amount, "x": x, "y": y}, 200)
    except Exception:
        amount = random.randrange(0, 25)
        x = random.randint(0, 100000000)
        y = random.randint(0, 100000000)
        try:
            task = add.delay(amount, x, y)
            return JSONResponse({"status": "ok", "taskId": task.id, "amount": amount, "x": x, "y": y}, 200)
        except Exception as e:
            return JSONResponse({"status": "error", "message": str(e)})

@app.post("/status")
async def task_status(request: Request):
    try:
        data = await request.json()
        if "taskID" not in data:
            return JSONResponse({"status": "specify correct json body"}, 400)
        task_id = data["taskID"]
        res = AsyncResult(task_id)
        return JSONResponse({"taskStatus": res.status}, 200)
    except Exception:
        return JSONResponse({"status": "invalid json body"}, 400)

@app.post("/project")
async def create_project(request: Request):
    try:
        data = await request.json()
        if "username" not in data:
            return JSONResponse({"status": "specify username in json body"}, 400)
        if "projectname" not in data:
            return JSONResponse({"status": "specify projectname in json body"}, 400)
        return JSONResponse({"status": "ok"}, 200)
    except Exception:
        return JSONResponse({"status": "invalid json body"}, 400)

@app.post("/user")
async def create_user(request: Request):
    try:
        data = await request.json()
        if "username" not in data:
            return JSONResponse({"status": "specify username in json body"}, 400)
        return JSONResponse({"status": "ok"}, 200)
    except Exception:
        return JSONResponse({"status": "invalid json body"}, 400)

@app.post("/train")
async def train(request: Request):
    try:
        data = await request.json()
        if "userID" not in data:
            return JSONResponse({"status": "specify userID in json body"}, 400)
        if "projectID" not in data:
            return JSONResponse({"status": "specify projectID in json body"}, 400)
        return JSONResponse({"status": "ok"}, 200)
    except Exception:
        return JSONResponse({"status": "invalid json body"}, 400)
