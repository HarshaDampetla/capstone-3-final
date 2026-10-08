from decimal import Decimal
import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.core.security import create_access_token
from src.db.models import UserModel, StockCatalogModel, PortfolioHoldingModel
from src.domain.models import UserRole, AccountState, StockStatus

client = TestClient(app)


def get_customer_auth_header(db_session, email="portfolio_customer@marketscope.com"):
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
@pytest.mark.ac("AC-09")
def test_ac_09_portfolio_stats_api(db_session):
    """Verify AC-09 API: Returns total_invested, current_value, absolute_pnl, and percent_pnl."""
    headers, customer = get_customer_auth_header(db_session, email="ac09_api_cust@marketscope.com")

    # Add stocks to catalog
    s1 = StockCatalogModel(symbol="AAPL", company_name="Apple", sector="Tech", exchange="NASDAQ", current_price=Decimal("180.00"), status=StockStatus.ACTIVE)
    s2 = StockCatalogModel(symbol="MSFT", company_name="Microsoft", sector="Tech", exchange="NASDAQ", current_price=Decimal("280.00"), status=StockStatus.ACTIVE)
    db_session.add(s1)
    db_session.add(s2)

    # Add holdings for customer: 10 AAPL (avg buy 150.00), 5 MSFT (avg buy 300.00)
    h1 = PortfolioHoldingModel(user_id=customer.id, symbol="AAPL", quantity=Decimal("10"), average_buy_price=Decimal("150.00"))
    h2 = PortfolioHoldingModel(user_id=customer.id, symbol="MSFT", quantity=Decimal("5"), average_buy_price=Decimal("300.00"))
    db_session.add(h1)
    db_session.add(h2)
    db_session.commit()

    res = client.get("/api/v1/portfolio/stats", headers=headers)
    assert res.status_code == 200
    data = res.json()

    assert data["customer_id"] == customer.id
    assert Decimal(str(data["total_invested"])) == Decimal("3000.00")
    assert Decimal(str(data["current_value"])) == Decimal("3200.00")
    assert Decimal(str(data["absolute_pnl"])) == Decimal("200.00")
    assert Decimal(str(data["percent_pnl"])) == Decimal("6.67")


@pytest.mark.integration
@pytest.mark.ac("AC-09")
def test_ac_09_empty_portfolio_stats_api(db_session):
    """Verify AC-09 API: Customer with 0 holdings returns zero metrics."""
    headers, customer = get_customer_auth_header(db_session, email="ac09_empty_cust@marketscope.com")

    res = client.get("/api/v1/portfolio/stats", headers=headers)
    assert res.status_code == 200
    data = res.json()

    assert data["customer_id"] == customer.id
    assert Decimal(str(data["total_invested"])) == Decimal("0.00")
    assert Decimal(str(data["current_value"])) == Decimal("0.00")
    assert Decimal(str(data["absolute_pnl"])) == Decimal("0.00")
    assert Decimal(str(data["percent_pnl"])) == Decimal("0.00")
