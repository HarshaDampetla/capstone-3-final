from decimal import Decimal
import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.core.security import create_access_token
from src.db.models import UserModel, StockCatalogModel, PortfolioHoldingModel, OrderModel
from src.domain.models import UserRole, AccountState, StockStatus, OrderStatus, OrderSide, OrderType

client = TestClient(app)


def get_customer_auth_header(db_session, email="analytics_cust@marketscope.com"):
    """Helper creating customer user in database and returning auth header."""
    customer = UserModel(
        email=email,
        hashed_password="hashed_password_example",
        role=UserRole.CUSTOMER,
        state=AccountState.ACTIVE,
        available_cash=Decimal("10000.0000"),
    )
    db_session.add(customer)
    db_session.commit()
    token = create_access_token(subject=customer.id, role=customer.role.value)
    return {"Authorization": f"Bearer {token}"}, customer


@pytest.mark.integration
@pytest.mark.ac("AC-10")
def test_ac_10_daily_top_gainers_and_losers_api(db_session):
    """Verify AC-10 API: Daily analytics returns top 5 gainers and top 5 losers for customer's holdings."""
    headers, customer = get_customer_auth_header(db_session, email="ac10_cust@marketscope.com")

    # Catalog stocks
    s1 = StockCatalogModel(symbol="WINNER", company_name="Winner Inc", sector="Tech", exchange="NASDAQ", current_price=Decimal("150.00"), status=StockStatus.ACTIVE)
    s2 = StockCatalogModel(symbol="LOSER", company_name="Loser Inc", sector="Energy", exchange="NYSE", current_price=Decimal("50.00"), status=StockStatus.ACTIVE)
    s3 = StockCatalogModel(symbol="NEUTRAL", company_name="Neutral Inc", sector="Tech", exchange="NASDAQ", current_price=Decimal("100.00"), status=StockStatus.ACTIVE)
    db_session.add_all([s1, s2, s3])

    # Customer holdings: WINNER (buy 100, curr 150 -> +50%), LOSER (buy 100, curr 50 -> -50%), NEUTRAL (buy 100, curr 100 -> 0%)
    h1 = PortfolioHoldingModel(user_id=customer.id, symbol="WINNER", quantity=Decimal("10"), average_buy_price=Decimal("100.00"))
    h2 = PortfolioHoldingModel(user_id=customer.id, symbol="LOSER", quantity=Decimal("10"), average_buy_price=Decimal("100.00"))
    h3 = PortfolioHoldingModel(user_id=customer.id, symbol="NEUTRAL", quantity=Decimal("10"), average_buy_price=Decimal("100.00"))
    db_session.add_all([h1, h2, h3])
    db_session.commit()

    res = client.get("/api/v1/analytics/daily", headers=headers)
    assert res.status_code == 200
    data = res.json()

    assert "top_gainers" in data and len(data["top_gainers"]) > 0
    assert "top_losers" in data and len(data["top_losers"]) > 0
    assert data["top_gainers"][0]["symbol"] == "WINNER"
    assert Decimal(str(data["top_gainers"][0]["percent_pnl"])) == Decimal("50.00")
    assert data["top_losers"][0]["symbol"] == "LOSER"
    assert Decimal(str(data["top_losers"][0]["percent_pnl"])) == Decimal("-50.00")


@pytest.mark.integration
def test_analytics_user_isolation_api(db_session):
    """Verify Customer A can ONLY see their own holdings analytics, not Customer B's."""
    headers_a, cust_a = get_customer_auth_header(db_session, email="cust_a_analytics@marketscope.com")
    headers_b, cust_b = get_customer_auth_header(db_session, email="cust_b_analytics@marketscope.com")

    # Add stock
    s1 = StockCatalogModel(symbol="PRIV", company_name="Private", sector="Tech", exchange="NASDAQ", current_price=Decimal("200.00"), status=StockStatus.ACTIVE)
    db_session.add(s1)

    # Customer A holds PRIV, Customer B holds nothing
    h_a = PortfolioHoldingModel(user_id=cust_a.id, symbol="PRIV", quantity=Decimal("5"), average_buy_price=Decimal("100.00"))
    db_session.add(h_a)
    db_session.commit()

    # Customer A sees PRIV
    res_a = client.get("/api/v1/analytics/daily", headers=headers_a)
    assert res_a.status_code == 200
    assert len(res_a.json()["top_gainers"]) == 1

    # Customer B sees empty lists
    res_b = client.get("/api/v1/analytics/daily", headers=headers_b)
    assert res_b.status_code == 200
    assert len(res_b.json()["top_gainers"]) == 0
    assert len(res_b.json()["top_losers"]) == 0


@pytest.mark.integration
def test_platform_analytics_and_settlement_queue_api(db_session):
    """Verify platform analytics endpoint returning status volume breakdown and settlement queue."""
    headers, customer = get_customer_auth_header(db_session, email="platform_admin@marketscope.com")

    # Create pending and executed orders
    o1 = OrderModel(user_id=customer.id, symbol="AAPL", side=OrderSide.BUY, order_type=OrderType.LIMIT, quantity=Decimal("2"), quote_price=Decimal("150"), status=OrderStatus.PENDING)
    o2 = OrderModel(user_id=customer.id, symbol="AAPL", side=OrderSide.SELL, order_type=OrderType.MARKET, quantity=Decimal("1"), quote_price=Decimal("155"), status=OrderStatus.EXECUTED)
    db_session.add_all([o1, o2])
    db_session.commit()

    res = client.get("/api/v1/analytics/platform", headers=headers)
    assert res.status_code == 200
    data = res.json()

    assert data["total_orders"] >= 2
    assert "volume_by_status" in data
    assert data["volume_by_status"]["PENDING"] >= 1
    assert data["volume_by_status"]["EXECUTED"] >= 1
    assert "settlement_queue" in data
    assert data["settlement_queue_length"] >= 1


@pytest.mark.integration
def test_synthetic_market_data_tick_api(db_session):
    """Verify synthetic market data price tick endpoint."""
    headers, customer = get_customer_auth_header(db_session, email="tick_user@marketscope.com")

    s1 = StockCatalogModel(symbol="TICK", company_name="Tick Inc", sector="Tech", exchange="NASDAQ", current_price=Decimal("100.00"), status=StockStatus.ACTIVE)
    db_session.add(s1)
    db_session.commit()

    res = client.post("/api/v1/market/tick", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["ticked_stocks_count"] >= 1
