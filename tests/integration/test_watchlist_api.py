import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.core.security import create_access_token
from src.db.models import UserModel
from src.domain.models import UserRole, AccountState

client = TestClient(app)


@pytest.mark.integration
@pytest.mark.ac("AC-04")
def test_ac_04_watchlist_api_creation_and_limit(db_session):
    """Verify AC-04 API: Customer watchlist creation and 10 watchlist limit."""
    customer = UserModel(email="cust_wl_api@marketscope.com", hashed_password="hash", role=UserRole.CUSTOMER, state=AccountState.ACTIVE)
    db_session.add(customer)
    db_session.commit()

    token = create_access_token(subject=customer.id, role=customer.role.value)
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Create 10 watchlists
    for i in range(1, 11):
        res = client.post(
            "/api/v1/watchlists",
            headers=headers,
            json={"name": f"Watchlist {i}", "symbols": ["AAPL"]}
        )
        assert res.status_code == 201
        assert res.json()["name"] == f"Watchlist {i}"
        assert res.json()["symbols"] == ["AAPL"]

    # 2. 11th creation attempt fails with HTTP 400
    res = client.post(
        "/api/v1/watchlists",
        headers=headers,
        json={"name": "Watchlist 11", "symbols": ["MSFT"]}
    )
    assert res.status_code == 400
    assert "limit reached" in res.json()["detail"].lower() or "cannot hold more than 10" in res.json()["detail"].lower()


@pytest.mark.integration
@pytest.mark.ac("AC-05")
def test_ac_05_watchlist_api_atomic_update_and_delete(db_session):
    """Verify AC-05 API: Watchlist atomic updates and deletion."""
    customer = UserModel(email="cust_atomic_api@marketscope.com", hashed_password="hash", role=UserRole.CUSTOMER, state=AccountState.ACTIVE)
    db_session.add(customer)
    db_session.commit()

    token = create_access_token(subject=customer.id, role=customer.role.value)
    headers = {"Authorization": f"Bearer {token}"}

    # Create watchlist
    res = client.post(
        "/api/v1/watchlists",
        headers=headers,
        json={"name": "Tech Watchlist", "symbols": ["AAPL", "MSFT"]}
    )
    assert res.status_code == 201
    wl_id = res.json()["id"]

    # Atomic Update
    res = client.put(
        f"/api/v1/watchlists/{wl_id}",
        headers=headers,
        json={"name": "Updated Tech", "symbols": ["NVDA", "TSLA"]}
    )
    assert res.status_code == 200
    assert res.json()["name"] == "Updated Tech"
    assert "NVDA" in res.json()["symbols"]

    # Delete Watchlist
    res = client.delete(f"/api/v1/watchlists/{wl_id}", headers=headers)
    assert res.status_code == 204


@pytest.mark.integration
def test_cross_customer_watchlist_isolation_api(db_session):
    """Verify security: Customer cannot modify another customer's watchlist via API (HTTP 403)."""
    cust1 = UserModel(email="cust1_iso@marketscope.com", hashed_password="hash", role=UserRole.CUSTOMER, state=AccountState.ACTIVE)
    cust2 = UserModel(email="cust2_iso@marketscope.com", hashed_password="hash", role=UserRole.CUSTOMER, state=AccountState.ACTIVE)
    db_session.add(cust1)
    db_session.add(cust2)
    db_session.commit()

    token1 = create_access_token(subject=cust1.id, role=cust1.role.value)
    token2 = create_access_token(subject=cust2.id, role=cust2.role.value)

    headers1 = {"Authorization": f"Bearer {token1}"}
    headers2 = {"Authorization": f"Bearer {token2}"}

    # Cust 1 creates watchlist
    res = client.post("/api/v1/watchlists", headers=headers1, json={"name": "Cust 1 List", "symbols": ["AAPL"]})
    wl_id = res.json()["id"]

    # Cust 2 attempts to get Cust 1's watchlist -> HTTP 403
    res = client.get(f"/api/v1/watchlists/{wl_id}", headers=headers2)
    assert res.status_code == 403

    # Cust 2 attempts to update Cust 1's watchlist -> HTTP 403
    res = client.put(f"/api/v1/watchlists/{wl_id}", headers=headers2, json={"name": "Hacked"})
    assert res.status_code == 403

    # Cust 2 attempts to delete Cust 1's watchlist -> HTTP 403
    res = client.delete(f"/api/v1/watchlists/{wl_id}", headers=headers2)
    assert res.status_code == 403
