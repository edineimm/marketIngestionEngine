from core.configs import DBBaseModel
from sqlalchemy import Column, Float, String, Integer, DateTime
from datetime import datetime, timezone


class MarketData(DBBaseModel):
    __tablename__ = "market_data"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), index=True, nullable=False)
    timestamp = Column(DateTime(timezone=True),
                       default=lambda: datetime.now(timezone.utc), index=True)
    open_price = Column(Float, nullable=False)
    high_price = Column(Float, nullable=False)
    low_price = Column(Float, nullable=False)
    close_price = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
