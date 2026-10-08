from decimal import Decimal
import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.core.security import create_access_token
from src.db.models import UserModel, StockCatalogModel
from src.domain.models import UserRole, AccountState, StockStatus

client = TestClient(app)


@pytest.mark.integration
@pytest.mark.ac("AC-03")
def test_ac_03_admin_stock_crud_api(db_session):
    """Verify AC-03 API: Admin CRUD operations and soft-delete endpoints."""
    admin = UserModel(email="admin_api_cat@marketscope.com", hashed_password="hash", role=UserRole.ADMIN, state=AccountState.ACTIVE)
    db_session.add(admin)
    db_session.commit()

    token = create_access_token(subject=admin.id, role=admin.role.value)
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Create Stock
    response = client.post(
        "/api/v1/admin/catalog",
        headers=headers,
        json={
            "symbol": "MSFT",
            "company_name": "Microsoft Corp",
            "sector": "Technology",
            "exchange": "NASDAQ",
            "current_price": "400.00"
        }
    )
    assert response.status_code == 201
    assert response.json()["symbol"] == "MSFT"
    assert response.json()["status"] == "ACTIVE"

    # 2. Update Stock
    response = client.put(
        "/api/v1/admin/catalog/MSFT",
        headers=headers,
        json={"current_price": "420.00"}
    )
    assert response.status_code == 200
    assert Decimal(response.json()["current_price"]) == Decimal("420.00")

    # 3. Soft Delete Stock
    response = client.delete("/api/v1/admin/catalog/MSFT", headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "DELETED"


@pytest.mark.integration
@pytest.mark.ac("AC-03")
def test_ac_03_customer_search_stocks_api(db_session):
    """Verify AC-03 API: Customer searching by symbol, sector, exchange."""
    customer = UserModel(email="cust_search_api@marketscope.com", hashed_password="hash", role=UserRole.CUSTOMER, state=AccountState.ACTIVE)
    db_session.add(customer)

    s1 = StockCatalogModel(symbol="AMZN", company_name="Amazon", sector="Consumer Cyclical", exchange="NASDAQ", current_price=Decimal("180.00"), status=StockStatus.ACTIVE)
    s2 = StockCatalogModel(symbol="JPM", company_name="JPMorgan", sector="Financial", exchange="NYSE", current_price=Decimal("200.00"), status=StockStatus.ACTIVE)
    db_session.add(s1)
    db_session.add(s2)
    db_session.commit()

    token = create_access_token(subject=customer.id, role=customer.role.value)
    headers = {"Authorization": f"Bearer {token}"}

    # Search by sector
    res = client.get("/api/v1/catalog?sector=Financial", headers=headers)
    assert res.status_code == 200
    items = res.json()
    assert len(items) == 1
    assert items[0]["symbol"] == "JPM"

    # Search by exchange
    res = client.get("/api/v1/catalog?exchange=NASDAQ", headers=headers)
    assert res.status_code == 200
    items = res.json()
    assert len(items) == 1
    assert items[0]["symbol"] == "AMZN"


@pytest.mark.integration
@pytest.mark.ac("AC-03")
def test_ac_03_customer_denied_admin_catalog_actions_api(db_session):
    """Verify AC-03 API: Customer attempting admin catalog modification receives HTTP 403."""
    customer = UserModel(email="cust_denied_cat@marketscope.com", hashed_password="hash", role=UserRole.CUSTOMER, state=AccountState.ACTIVE)
    db_session.add(customer)
    db_session.commit()

    token = create_access_token(subject=customer.id, role=customer.role.value)
    headers = {"Authorization": f"Bearer {token}"}

    # Attempt create stock
    res = client.post(
        "/api/v1/admin/catalog",
        headers=headers,
        json={"symbol": "NFLX", "company_name": "Netflix", "sector": "Media", "exchange": "NASDAQ", "current_price": "600.00"}
    )
    assert res.status_code == 403

    # Attempt soft delete stock
    res = client.delete("/api/v1/admin/catalog/AMZN", headers=headers)
    assert res.status_code == 403
