import asyncio
import httpx
from datetime import datetime
from core.configs import settings

API_URL = f"http://localhost:8000{settings.API_V1_STR}/market-data/bulk"
BINANCE_BASE_URL = "https://api.binance.com/api/v3/klines"
SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "ADAUSDT", "DOTUSDT", "LINKUSDT"]


async def fetch_symbol_data(client: httpx.AsyncClient, symbol: str):
    """Busca dados de um único símbolo na Binance."""
    params = {"symbol": symbol, "interval": "1m", "limit": 5}
    print(f"🔍 Coletando {symbol}...")

    response = await client.get(BINANCE_BASE_URL, params=params)
    if response.status_code != 200:
        print(f"❌ Erro ao buscar {symbol}: {response.text}")
        return []

    data = response.json()
    ticks = []
    for candle in data:
        ticks.append({
            "symbol": symbol,
            "timestamp": datetime.fromtimestamp(candle[0] / 1000).isoformat(),
            "open_price": float(candle[1]),
            "high_price": float(candle[2]),
            "low_price": float(candle[3]),
            "close_price": float(candle[4]),
            "volume": float(candle[5])
        })
    return ticks


async def run_multi_ingestion():
    async with httpx.AsyncClient() as client:
        # 1. Cria as tarefas para todos os símbolos simultaneamente
        tasks = [fetch_symbol_data(client, s) for s in SYMBOLS]

        # 2. Executa em paralelo (Fan-in)
        results = await asyncio.gather(*tasks)

        # 3. Achata a lista de listas em uma única lista gigante
        total_payload = [tick for sublist in results for tick in sublist]

        if not total_payload:
            print("⚠️ Nenhum dado coletado.")
            return

        # 4. Envia tudo para o SEU backend em uma única transação
        print(
            f"📦 Enviando total de {len(total_payload)} registros para o PostgreSQL...")
        post_res = await client.post(API_URL, json=total_payload)

        if post_res.status_code == 201:
            print("✅ Sucesso! Carteira sincronizada no banco de dados.")
        else:
            print(f"❌ Falha na ingestão: {post_res.text}")

if __name__ == "__main__":
    start_time = datetime.now()
    asyncio.run(run_multi_ingestion())
    end_time = datetime.now()
    print(f"⏱️ Tempo total de execução: {end_time - start_time}")
