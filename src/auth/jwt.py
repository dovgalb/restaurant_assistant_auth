from fastapi_users.authentication import JWTStrategy, BearerTransport, AuthenticationBackend

from src.config.configs import get_settings

settings = get_settings()

SECRET = settings.secret

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

