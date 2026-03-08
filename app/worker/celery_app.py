# app/worker/celery_app.py
from celery import Celery

# O Redis atua como o intermediário (Broker) que guarda a fila de tarefas
celery_app = Celery(
    "market_worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# Autodiscover tasks no nosso diretório
celery_app.autodiscover_tasks(["app.worker"])
