from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from celery_worker import create_task

tasks_router = APIRouter()


@tasks_router.post(path="/sample")
def run_task(data=Body(...)):
    amount = int(data['amount'])
    x = data['x']
    y = data['y']
    task = create_task.delay(amount, x, y)
    return JSONResponse({'Calculation': task.get()})


@tasks_router.get("/test-get")
async def get_data():
    return JSONResponse({"data": "helloo world"})