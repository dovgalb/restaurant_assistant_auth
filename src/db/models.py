from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID

from src.db.base import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass

