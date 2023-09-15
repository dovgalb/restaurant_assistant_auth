import os
import smtplib
import time
from email.message import EmailMessage

from celery import Celery
from dotenv import load_dotenv

load_dotenv('./src/config/.env')
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get('CELERY_BROKER_URL')
celery.conf.result_backend = os.environ.get('CELERY_RESULT_BACKEND')


@celery.task(name="create_task")
def create_task(time_delay, b, c):
    time.sleep(time_delay)
    return b + c


def get_email_for_registration(username: str):
    email = EmailMessage()
    email['Subject'] = 'Регистрация завершена'
    email['From'] = SMTP_USER
    email['To'] = SMTP_USER

    email.set_content(
        '<div>'
        f'<h1>Congratulations! You are account was creat</h1>'
        '</div>',
        subtype='html'
    )
    return email


@celery.task(name="send_email")
def send_email_about_success_registration(username: str, delay):
    email = get_email_for_registration(username)
    time.sleep(delay)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
