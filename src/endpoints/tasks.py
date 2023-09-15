from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from celery_worker import create_task

tasks_router = APIRouter()


@tasks_router.post(path="/sample")
def run_task(amount: int, x: int, y: int):
    """
    представление для симуляции длительной задачи
    """
    amount = amount
    x = x
    y = y
    task = create_task.delay(amount, x, y)
    return JSONResponse({'Calculation': task.get()})


@tasks_router.get("/test-get")
async def get_data():
    return JSONResponse({"data": "helloo world"})

