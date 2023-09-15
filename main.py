import uvicorn
from fastapi import FastAPI

from src.config.configs import get_settings
from src.endpoints.users import user_router
from src.endpoints.tasks import tasks_router

app = FastAPI(
    title="Restaurant Assistant Auth"
)

app.include_router(user_router, tags=["auth"])
app.include_router(tasks_router, prefix="/tasks", tags=['/tasks'])

settings = get_settings()

if __name__ == "__main__":
    uvicorn.run(app, host=settings.service_host, port=settings.service_port, log_level="info")
