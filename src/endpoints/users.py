import uuid

from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from src.auth.jwt import auth_backend
from src.db.managers import get_user_manager
from src.db.models import User
from src.schemas.users import UserRead, UserCreate

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

user_router = APIRouter()

user_router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)

user_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
