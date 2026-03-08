import asyncio
from worker.celery_app import celery_app
from ingest_multi import run_multi_ingestion


@celery_app.task(bind=True, max_retries=3)
def fetch_and_store_market_data(self):
    """
    Tarefa assíncrona gerenciada pelo Celery.
    Se a Binance rejeitar a conexão, o Celery tenta de novo automaticamente até 3 vezes.
    """
    try:
        print("🤖 [WORKER] Iniciando coleta de dados de múltiplos ativos...")
        # Executa a lógica assíncrona pesada de bater na Binance e salvar no Postgres
        asyncio.run(run_multi_ingestion())
        return "Coleta concluída com sucesso."

    except Exception as exc:
        print(f"❌ [WORKER] Falha na coleta. Tentando novamente... Erro: {exc}")
        # A resiliência que as empresas de ponta exigem:
        raise self.retry(exc=exc, countdown=60)  # Tenta de novo em 60 segundos
