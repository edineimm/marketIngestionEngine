from fastapi import APIRouter
from api.v1.endpoints import market_data
from core.configs import settings

api_router = APIRouter()
api_router.include_router(market_data.router)
