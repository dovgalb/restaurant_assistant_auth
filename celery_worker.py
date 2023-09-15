import os
import time

from celery import Celery
from dotenv import load_dotenv

load_dotenv('./src/config/.env')

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get('CELERY_BROKER_URL')
celery.conf.result_backend = os.environ.get('CELERY_RESULT_BACKEND')


@celery.task(name="create_task")
def create_task(time_delay, b, c):
    time.sleep(time_delay)
    return b + c
