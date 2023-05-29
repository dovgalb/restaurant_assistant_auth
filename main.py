import uvicorn
from fastapi import FastAPI

from src.config.configs import get_settings
from src.endpoints.users import user_router

app = FastAPI()

app.include_router(user_router)

settings = get_settings()

if __name__ == "__main__":
    uvicorn.run(app, host=settings.service_host, port=settings.service_port, log_level="info")
