from celery import Celery
import redis
from datetime import timedelta
from celery.schedules import crontab

celery_app = Celery(
    "app", 
    broker = "redis://localhost:6379/0",
    backend = "redis://localhost:6379/0",
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