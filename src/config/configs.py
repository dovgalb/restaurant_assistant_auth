"""
Настройки приложения
"""
# pylint: disable = too-few-public-methods, no-self-use, E0213, E0611
from functools import lru_cache
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseSettings, FilePath, PostgresDsn, validator

APP_DIR = Path(__file__).resolve(strict=True).parent.parent


class Settings(BaseSettings):
    """
    Класс настроек приложения
    """

    # DEBUG
    debug: bool = True
    allow_unauthorized: bool = False
    https_proxy_enabled: bool = True

    # SERVICE
    service_host: str = "0.0.0.0"
    service_port: int = 8000
    service_title: str = "api"

    # AUTH

    secret: str = "secret"

    # DB
    postgres_host: str = "127.0.0.1"
    postgres_port: str = "5432"
    postgres_user: str = "user"
    postgres_password: str = "pass"
    postgres_db: str = "name"
    db_future: bool = True
    db_pool_recycle: int = 30 * 60
    db_echo: bool = True

    database: dict[str, Any] = {}

    directory_host: str = "127.0.0.1"
    directory_port: str = "80"

    # REDIS

    celery_broker_url: str = "redis://redis:6379/0"
    celery_result_backend: str = "redis://redis:6379/0"

    @validator("database", pre=True)
    def pass_database_settings(
            cls, value: Optional[str], values: dict[str, Any]
    ) -> dict[str, Any]:
        """Прокидывает настройки БД"""
        if value and isinstance(value, dict):
            return value

        return {
            "url": PostgresDsn.build(
                scheme="postgresql+asyncpg",
                user=values["postgres_user"],
                password=values["postgres_password"],
                host=values["postgres_host"],
                port=values["postgres_port"],
                path=f"/{values['postgres_db']}",
            ),
            "future": values["db_future"],
            "pool_recycle": values["db_pool_recycle"],
            "echo": values["db_echo"],
        }

    # Logging
    log_level: str = "INFO"
    fluentd_host: str = ""
    fluentd_port: int = 24224
    fluentd_tag: str = "api-server"

    logging: dict[str, Any] = {}

    @validator("logging", pre=True)
    def pass_logging_settings(
            cls, value: Optional[str], values: dict[str, Any]
    ) -> dict[str, Any]:
        """Прокидывает настройки логгера"""
        if value and isinstance(value, dict):
            return value

        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "console": {
                    "format": (
                        "%(name)-12s %(asctime)s %(levelname)-8s "
                        "%(filename)s:%(funcName)s %(message)s"
                    ),
                    "datefmt": "%d.%m.%y %H:%M:%S",
                },
                "logstash": {"()": "app.utils.logger.logger.LogsFormatter"},
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "DEBUG",
                    "formatter": "console",
                    "stream": "ext://sys.stdout",
                },
                "logstash": {
                    "class": "app.utils.logger.logger.LogsHandler",
                    "tag": values["fluentd_tag"],
                    "host": values["fluentd_host"],
                    "port": values["fluentd_port"],
                    "level": values["log_level"],
                    "formatter": "logstash",
                },
            },
            "loggers": {
                "root": {"level": "WARNING", "handlers": ["console"]},
                "app": {"level": "DEBUG", "handlers": ["console", "logstash"]},
            },
        }

    class Config:
        """
        Класс pydantic для определения дополнительных свойств класса настроек
        """

        env_file = str(APP_DIR / "config" / ".env")


@lru_cache()
def get_settings() -> Settings:
    """Инициализирует класс настроек"""
    return Settings()
