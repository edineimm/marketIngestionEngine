# 📈 Market Ingestor Engine

An asynchronous, distributed, and enterprise-grade data ingestion engine designed for financial market backtesting and predictive data modeling.

This system architecture decouples the API layer from heavy I/O operations by implementing a Producer-Consumer pattern using a message broker and background workers, ensuring high availability and zero-blocking execution.

---

## 🏗️ System Architecture

The architecture simulates a production-ready microservices environment, completely containerized.

```text
User / Cron               [ FastAPI ] (Port 8000)
   |                          |
   | (Triggers/Requests)      | (Asynchronous DB Writes)
   v                          v
[ Celery Beat ] --------> [ PostgreSQL 16 ] (Port 5432)
(Scheduler)                   ^
   |                          | (Saves OHLCV data)
   | (Enqueues Tasks)         |
   v                          |
[ Redis ] <--------------- [ Celery Worker ]
(Message Broker)              | (Fetches Data async)
                              v
                        [ External Oracles / Binance API ]

[ Flower ] (Port 5555) -> Monitors Redis and Worker health in real-time.
```

---

## 🚀 Tech Stack

| Layer | Technology |
|---|---|
| API Framework | Python 3.11, FastAPI, Pydantic |
| Database & ORM | PostgreSQL 16, SQLAlchemy (Async Mode) |
| Message Broker & Cache | Redis |
| Background Task Queue | Celery, Celery Beat |
| Observability | Flower |
| Infrastructure | Docker, Docker Compose |

---

## ⚙️ Quick Start / Run Book

Follow this execution script to clean previous instances, build the environment, and test the API endpoints.

**1. Navigate to the project directory:**

```bash
cd marketIngestionEngine/app
```

**2. Clean up previous Docker artifacts (Troubleshooting / Fresh Start):**

```bash
docker container prune -f
docker network prune -f
```

> ⚠️ If you encounter database permission errors, tear down volumes completely:
> ```bash
> docker compose down -v
> ```

**3. Build and spin up the microservices:**

```bash
docker compose up --build
```

**4. Monitor and Test (open in your browser):**

| Service | URL |
|---|---|
| Observability Dashboard (Flower) | http://localhost:5555 |
| Interactive API Docs (Swagger) | http://localhost:8000/docs |
| Fetch All Market Data | http://localhost:8000/api/v1/market-data/ |
| Fetch Specific Asset (BTCUSDT) | http://localhost:8000/api/v1/market-data/BTCUSDT |

**5. Trigger a manual data sync:**

```bash
curl -X POST http://localhost:8000/api/v1/market-data/backtest/sync-data
```

**6. Gracefully shut down the engine:**

```bash
docker compose down
```

---

## 📊 Core Features

- **Async Data Ingestion** — Fetches real-time market data (OHLCV) concurrently using `httpx` and `asyncio`, eliminating I/O bottlenecks.
- **Autonomous Synchronization** — `Celery Beat` acts as a distributed clock, triggering portfolio data updates every minute without manual intervention.
- **Fault Tolerance** — Built-in retry mechanisms (up to 3 attempts, 60s cooldown) for external API rate-limiting or network failures.
- **Database Lifespan Management** — Automated schema generation upon application startup using FastAPI's lifespan context managers.
- **Full Observability** — Flower dashboard provides real-time monitoring of task throughput, worker health, and broker queue depth.

---

## 🗂️ Project Structure

```
app/
├── api/
│   └── v1/
│       ├── api.py
│       └── endpoints/
│           └── market_data.py
├── core/
│   ├── configs.py
│   ├── database.py
│   └── deps.py
├── models/
│   └── market_data.py
├── schemas/
│   └── market_data.py
├── worker/
│   ├── celery_app.py
│   └── tasks.py
├── ingest_multi.py
├── main.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/market-data/` | Retrieve all market data |
| `GET` | `/api/v1/market-data/{symbol}` | Retrieve data by symbol (optional `?minutes=60`) |
| `POST` | `/api/v1/market-data/` | Insert a single market data record |
| `POST` | `/api/v1/market-data/bulk` | Insert multiple records in one transaction |
| `POST` | `/api/v1/market-data/backtest/sync-data` | Trigger async Binance ingestion via Celery |
| `PUT` | `/api/v1/market-data/{symbol}` | Update market data by symbol |
| `DELETE` | `/api/v1/market-data/{symbol}` | Delete market data by symbol |
