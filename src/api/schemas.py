from decimal import Decimal
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from src.domain.models import UserRole, AccountState, StockStatus, OrderType, OrderSide, OrderStatus


# Auth & User Schemas
class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)


class RoleUpdateRequest(BaseModel):
    target_role: UserRole


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    role: UserRole
    state: AccountState
    available_cash: Decimal
    created_at: datetime


# Stock Catalog Schemas
class StockCreateRequest(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=20)
    company_name: str
    sector: str
    exchange: str
    current_price: Decimal = Field(..., gt=Decimal("0"))


class StockUpdateRequest(BaseModel):
    company_name: Optional[str] = None
    sector: Optional[str] = None
    exchange: Optional[str] = None
    current_price: Optional[Decimal] = Field(None, gt=Decimal("0"))


class StockResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    symbol: str
    company_name: str
    sector: str
    exchange: str
    current_price: Decimal
    status: StockStatus


# Watchlist Schemas
class WatchlistCreateRequest(BaseModel):
    name: str = Field(..., min_length=1)
    symbols: List[str] = Field(..., min_length=1)


class WatchlistResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    symbols: List[str]
    created_at: datetime

    @field_validator("symbols", mode="before")
    @classmethod
    def serialize_symbols(cls, v):
        if isinstance(v, list):
            res = []
            for item in v:
                if hasattr(item, "symbol"):
                    res.append(item.symbol)
                elif isinstance(item, str):
                    res.append(item)
            return res
        return v


# Order Schemas
class OrderCreateRequest(BaseModel):
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: Decimal = Field(..., gt=Decimal("0"))
    quote_price: Decimal = Field(..., gt=Decimal("0"))


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: Decimal
    quote_price: Decimal
    status: OrderStatus
    created_at: datetime


# Portfolio & Analytics Schemas
class PortfolioStatsResponse(BaseModel):
    customer_id: int
    total_invested: Decimal
    current_value: Decimal
    absolute_pnl: Decimal
    percent_pnl: Decimal


class GainersLosersResponse(BaseModel):
    top_gainers: List[dict]
    top_losers: List[dict]
