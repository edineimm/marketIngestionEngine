# app/worker/celery_app.py
from celery import Celery
from celery.schedules import crontab

# O Redis atua como o intermediário (Broker) que guarda a fila de tarefas
celery_app = Celery(
    "market_worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # Agendamento periódico via Celery Beat
    beat_schedule={
        "fetch-market-data-every-minute": {
            "task": "worker.tasks.fetch_and_store_market_data",
            "schedule": crontab(minute="*/1"),  # a cada 1 minuto
        },
    },
)

# Autodiscover tasks no nosso diretório
celery_app.autodiscover_tasks(["worker"])
