from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional


class UserRole(str, Enum):
    CUSTOMER = "CUSTOMER"
    ADMIN = "ADMIN"
    SUSPENDED = "SUSPENDED"


class AccountState(str, Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"


class StockStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DELETED = "DELETED"
    DELISTED = "DELISTED"


class OrderType(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"


class OrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    EXECUTED = "EXECUTED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"


@dataclass
class CustomerBalance:
    customer_id: int
    available_cash: Decimal
    currency: str = "USD"

    def __post_init__(self):
        if not isinstance(self.available_cash, Decimal):
            raise TypeError("available_cash must be a Decimal")


@dataclass
class OrderEntity:
    order_id: int
    customer_id: int
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: Decimal
    quote_price: Decimal
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        if not isinstance(self.quantity, Decimal):
            raise TypeError("quantity must be a Decimal")
        if not isinstance(self.quote_price, Decimal):
            raise TypeError("quote_price must be a Decimal")


@dataclass
class PortfolioStats:
    customer_id: int
    total_invested: Decimal
    current_value: Decimal
    absolute_pnl: Decimal
    percent_pnl: Decimal

    def __post_init__(self):
        for attr in ("total_invested", "current_value", "absolute_pnl", "percent_pnl"):
            if not isinstance(getattr(self, attr), Decimal):
                raise TypeError(f"{attr} must be a Decimal")
