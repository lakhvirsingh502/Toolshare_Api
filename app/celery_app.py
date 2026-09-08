from celery import Celery
import redis
from datetime import timedelta
from celery.schedules import crontab
from dotenv import load_dotenv
import os
load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")

celery_app = Celery(
    "app", 
    broker = REDIS_URL,
    backend = REDIS_URL,
    include=["app.tasks"]
)
celery_app.conf.timezone ="America/Toronto"
celery_app.conf.beat_schedule = {
    "run-beat-test-every-10-seconds":{
        "task":"app.tasks.beat_test",
        "schedule": crontab(hour=19,minute=00),
    }
}
celery_app.conf.beat_schedule = {
    "test_beat_every_10_seconds":{
        "task":"app.tasks.send_reservation_reminders",
        "schedule":crontab(hour=7,minute=00)
    }
}
celery_app.conf.beat_schedule = {
    "schedule-everyday":{
        "task":"app.tasks.expired_reservations",
        "schedule": crontab(hour=9, minute=00)
    }
}