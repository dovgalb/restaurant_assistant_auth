import uuid

from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers

from src.auth.jwt import auth_backend
from src.db.managers import get_user_manager
from src.db.models import User
from src.schemas.users import UserRead, UserCreate

from celery_worker import send_email_about_success_registration

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()

user_router = APIRouter()

user_router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)

user_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


@user_router.get('/dashboard')
def get_email_notification(delay: int, user=Depends(current_user)):
    send_email_about_success_registration.delay(user.email, delay)
    return {
        "status": 200,
        "data": 'Letter was send',
        "details": f"получатель {current_user}"
    }
