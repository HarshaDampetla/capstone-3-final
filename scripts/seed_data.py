"""Synthetic Data Seeder Script for MarketScope (BC-AINE-006).

Populates local database with synthetic initial users, stocks, watchlists, holdings, and orders.
SYNTHETIC DATA ONLY — Zero real financial or personal customer data used.
"""

import sys
import os
from decimal import Decimal
from datetime import datetime, timezone

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.database import SessionLocal, Base, engine
from src.core.security import get_password_hash
from src.db.models import (
    UserModel,
    StockCatalogModel,
    WatchlistModel,
    WatchlistSymbolModel,
    OrderModel,
    PortfolioHoldingModel,
)
from src.domain.models import UserRole, AccountState, StockStatus, OrderType, OrderSide, OrderStatus


def seed_database():
    print("[INFO] Initializing MarketScope database tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Clear existing seed data
        print("[INFO] Clearing old database records...")
        db.query(WatchlistSymbolModel).delete()
        db.query(WatchlistModel).delete()
        db.query(PortfolioHoldingModel).delete()
        db.query(OrderModel).delete()
        db.query(StockCatalogModel).delete()
        db.query(UserModel).delete()
        db.commit()

        # 2. Seed Synthetic Users
        print("[INFO] Seeding synthetic users (Admin & Customers)...")
        admin = UserModel(
            email="admin@marketscope.com",
            hashed_password=get_password_hash("AdminPassword123!"),
            role=UserRole.ADMIN,
            state=AccountState.ACTIVE,
            available_cash=Decimal("100000.0000"),
        )
        cust1 = UserModel(
            email="customer1@marketscope.com",
            hashed_password=get_password_hash("CustomerPassword123!"),
            role=UserRole.CUSTOMER,
            state=AccountState.ACTIVE,
            available_cash=Decimal("10000.0000"),
        )
        cust2 = UserModel(
            email="customer2@marketscope.com",
            hashed_password=get_password_hash("CustomerPassword123!"),
            role=UserRole.CUSTOMER,
            state=AccountState.ACTIVE,
            available_cash=Decimal("25000.0000"),
        )
        db.add_all([admin, cust1, cust2])
        db.commit()
        db.refresh(cust1)
        db.refresh(cust2)

        # 3. Seed Synthetic Stock Catalog
        print("[INFO] Seeding synthetic stock catalog...")
        stocks = [
            StockCatalogModel(symbol="AAPL", company_name="Apple Inc", sector="Technology", exchange="NASDAQ", current_price=Decimal("180.0000"), status=StockStatus.ACTIVE),
            StockCatalogModel(symbol="MSFT", company_name="Microsoft Corp", sector="Technology", exchange="NASDAQ", current_price=Decimal("280.0000"), status=StockStatus.ACTIVE),
            StockCatalogModel(symbol="GOOGL", company_name="Alphabet Inc", sector="Technology", exchange="NASDAQ", current_price=Decimal("175.0000"), status=StockStatus.ACTIVE),
            StockCatalogModel(symbol="AMZN", company_name="Amazon.com Inc", sector="Consumer Cyclical", exchange="NASDAQ", current_price=Decimal("185.0000"), status=StockStatus.ACTIVE),
            StockCatalogModel(symbol="NVDA", company_name="NVIDIA Corp", sector="Technology", exchange="NASDAQ", current_price=Decimal("120.0000"), status=StockStatus.ACTIVE),
            StockCatalogModel(symbol="JPM", company_name="JPMorgan Chase & Co", sector="Financial", exchange="NYSE", current_price=Decimal("200.0000"), status=StockStatus.ACTIVE),
            StockCatalogModel(symbol="TSLA", company_name="Tesla Inc", sector="Consumer Cyclical", exchange="NASDAQ", current_price=Decimal("210.0000"), status=StockStatus.ACTIVE),
        ]
        db.add_all(stocks)
        db.commit()

        # 4. Seed Synthetic Watchlists
        print("[INFO] Seeding synthetic watchlists...")
        wl1 = WatchlistModel(user_id=cust1.id, name="Tech Leaders")
        db.add(wl1)
        db.flush()

        s1 = WatchlistSymbolModel(watchlist_id=wl1.id, symbol="AAPL")
        s2 = WatchlistSymbolModel(watchlist_id=wl1.id, symbol="MSFT")
        s3 = WatchlistSymbolModel(watchlist_id=wl1.id, symbol="NVDA")
        db.add_all([s1, s2, s3])
        db.commit()

        # 5. Seed Synthetic Portfolio Holdings
        print("[INFO] Seeding synthetic portfolio holdings...")
        h1 = PortfolioHoldingModel(user_id=cust1.id, symbol="AAPL", quantity=Decimal("10.0000"), average_buy_price=Decimal("150.0000"))
        h2 = PortfolioHoldingModel(user_id=cust1.id, symbol="MSFT", quantity=Decimal("5.0000"), average_buy_price=Decimal("300.0000"))
        db.add_all([h1, h2])
        db.commit()

        # 6. Seed Synthetic Orders
        print("[INFO] Seeding synthetic trade orders...")
        o1 = OrderModel(
            user_id=cust1.id,
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            quantity=Decimal("10.0000"),
            quote_price=Decimal("150.0000"),
            status=OrderStatus.EXECUTED,
            created_at=datetime.now(timezone.utc),
        )
        o2 = OrderModel(
            user_id=cust1.id,
            symbol="MSFT",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            quantity=Decimal("5.0000"),
            quote_price=Decimal("300.0000"),
            status=OrderStatus.EXECUTED,
            created_at=datetime.now(timezone.utc),
        )
        o3 = OrderModel(
            user_id=cust1.id,
            symbol="GOOGL",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            quantity=Decimal("2.0000"),
            quote_price=Decimal("170.0000"),
            status=OrderStatus.PENDING,
            created_at=datetime.now(timezone.utc),
        )
        db.add_all([o1, o2, o3])
        db.commit()

        print("[SUCCESS] Synthetic database seeding completed successfully!")
        print("   Admin Login:    admin@marketscope.com / AdminPassword123!")
        print("   Customer Login: customer1@marketscope.com / CustomerPassword123!")
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Seeding error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
