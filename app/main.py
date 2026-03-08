from fastapi import FastAPI
from core.configs import settings
from api.v1.api import api_router
from core.database import engine
from core.configs import DBBaseModel
import models.__all_models  # garante que todos os modelos são registrados

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(DBBaseModel.metadata.create_all)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info", reload=True)
