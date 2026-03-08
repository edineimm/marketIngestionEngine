from datetime import timedelta, datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.market_data import MarketData
from schemas.market_data import MarketDataSchema
from core.deps import get_session

from worker.tasks import fetch_and_store_market_data

router = APIRouter(prefix="/market-data", tags=["Market Data"])

# POST endpoint to create market data


@router.post("/", response_model=MarketDataSchema, status_code=status.HTTP_201_CREATED)
async def post_market_data(market_data: MarketDataSchema, db: AsyncSession = Depends(get_session)):
    new_market_data = MarketData(**market_data.dict())
    db.add(new_market_data)
    await db.commit()
    await db.refresh(new_market_data)
    return new_market_data


# POST endpoint to create market data in bulk
@router.post("/bulk", response_model=List[MarketDataSchema], status_code=status.HTTP_201_CREATED)
async def post_market_data_bulk(market_data_list: List[MarketDataSchema], db: AsyncSession = Depends(get_session)):
    new_market_data_list = [MarketData(**market_data.dict())
                            for market_data in market_data_list]
    db.add_all(new_market_data_list)
    await db.commit()
    for market_data in new_market_data_list:
        await db.refresh(market_data)
    return new_market_data_list

# GET endpoint to retrieve all market data


@router.get("/", response_model=List[MarketDataSchema])
async def get_market_data(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(MarketData)
        result = await session.execute(query)
        list = result.scalars().all()
        return list

# GET endpoint to retrieve market data by symbol


@router.get("/{symbol}", response_model=List[MarketDataSchema])
async def get_market_data_by_symbol(symbol: str, minutes: Optional[int] = 60, db: AsyncSession = Depends(get_session)):
    time_threshold = datetime.now(timezone.utc) - timedelta(minutes=minutes)
    async with db as session:
        query = select(MarketData).where(MarketData.symbol == symbol).where(
            MarketData.timestamp >= time_threshold).order_by(MarketData.timestamp.desc())
        result = await session.execute(query)
        market_data = result.scalars().all()
        if market_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Market data from {MarketData.symbol} not found")
        return market_data

# PUT endpoint to update market data by symbol


@router.put("/{symbol}", response_model=MarketDataSchema)
async def update_market_data(symbol: str, market_data: MarketDataSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(MarketData).where(MarketData.symbol == symbol)
        result = await session.execute(query)
        existing_market_data = result.scalar_one_or_none()
        if existing_market_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Market data from {symbol} not found")
        for key, value in market_data.dict().items():
            setattr(existing_market_data, key, value)
        await session.commit()
        await session.refresh(existing_market_data)
        return existing_market_data

# DELETE endpoint to delete market data by symbol


@router.delete("/{symbol}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_market_data(symbol: str, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(MarketData).where(MarketData.symbol == symbol)
        result = await session.execute(query)
        existing_market_data = result.scalar_one_or_none()
        if existing_market_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Market data from {symbol} not found")
        await session.delete(existing_market_data)
        await session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/backtest/sync-data")
async def trigger_data_sync():
    # Isso manda a tarefa para o Redis e responde imediatamente ao usuário (em 5 milissegundos)
    task = fetch_and_store_market_data.delay()

    return {
        "message": "Sincronização de dados iniciada em background.",
        "task_id": task.id
    }
