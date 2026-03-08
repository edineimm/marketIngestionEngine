from pydantic import Field
from pydantic import BaseModel as SChemaBaseModel
from datetime import datetime


class MarketDataSchema(SChemaBaseModel):
    symbol: str = Field(..., max_length=20)
    timestamp: datetime
    open_price: float = Field(..., gt=0)
    high_price: float = Field(..., gt=0)
    low_price: float = Field(..., gt=0)
    close_price: float = Field(..., gt=0)
    volume: float = Field(..., ge=0)

    class Config:
        from_attributes = True
