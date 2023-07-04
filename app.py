import random
from typing import Optional
from pydantic import BaseModel
from datetime import datetime as dt
from fastapi import FastAPI, Request
from celery.result import AsyncResult
from fastapi.responses import JSONResponse
from fastapi.background import BackgroundTasks
from sqlmodel import SQLModel, Field, create_engine, Session, select
from tasks import add

app = FastAPI()
engine = create_engine("sqlite://")


class Transaction(SQLModel, table=True):
    id: int = Field(primary_key=True)
    taskID: str
    amount: float
    x: float
    y: float
    time: dt = dt.now()


class Data(BaseModel):
    amount: Optional[int | float] = random.randint(1, 25)
    x: Optional[int | float] = random.randint(0, 100000000)
    y: Optional[int | float] = random.randint(0, 100000000)


def insert_transaction(
    taskID: str, amount: int | float, x: int | float, y: int | float, time: dt
):
    with Session(engine) as session:
        trans = Transaction(taskID=taskID, amount=amount, x=x, y=y, time=time)
        session.add(trans)
        session.commit()
        session.close()


async def read_transactions():
    with Session(engine) as session:
        statement = select(Transaction)
        transactions = session.exec(statement)
        outs = []
        for transaction in transactions:
            outs.append(transaction.taskID)
        session.close()
    return outs


@app.on_event("startup")
async def start_up():
    SQLModel.metadata.create_all(engine)


@app.get("/")
async def index():
    return JSONResponse({"status": "ok"}, 200)


@app.post("/task")
async def create_task(data: Data, request: Request, bg: BackgroundTasks):
    task = add.delay(data.amount, data.x, data.y)
    bg.add_task(insert_transaction, task.id, data.amount, data.x, data.y, dt.now())
    return JSONResponse(
        {
            "taskId": task.id,
            "amount": data.amount,
            "x": data.x,
            "y": data.y,
        },
        200,
    )


@app.get("/status/{task_id}")
async def task_status(request: Request, task_id: str):
    return JSONResponse({"taskStatus": AsyncResult(task_id).status}, 200)


@app.get("/output/{task_id}")
async def task_output(request: Request, task_id: str):
    return JSONResponse({"taskStatus": AsyncResult(task_id).result}, 200)


@app.get("/transactions")
async def transaction(request: Request):
    outs = await read_transactions()
    return JSONResponse(outs, 200)
