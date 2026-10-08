from decimal import Decimal
import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.core.security import create_access_token
from src.db.models import UserModel
from src.domain.models import UserRole, AccountState

client = TestClient(app)


def get_customer_auth_header(db_session, email="customer_order@marketscope.com", available_cash=Decimal("10000.0000"), state=AccountState.ACTIVE):
    """Helper creating customer user in database and returning auth header."""
    customer = UserModel(
        email=email,
        hashed_password="hashed_password_example",
        role=UserRole.CUSTOMER if state == AccountState.ACTIVE else UserRole.SUSPENDED,
        state=state,
        available_cash=available_cash,
    )
    db_session.add(customer)
    db_session.commit()
    token = create_access_token(subject=customer.id, role=customer.role.value)
    return {"Authorization": f"Bearer {token}"}, customer


@pytest.mark.integration
@pytest.mark.ac("AC-06")
def test_ac_06_order_placement_api(db_session):
    """Verify AC-06: Customer places BUY/SELL orders (MARKET & LIMIT) in PENDING status with server timestamp."""
    headers, customer = get_customer_auth_header(db_session, email="ac06_cust@marketscope.com")

    # 1. LIMIT BUY
    payload_limit_buy = {
        "symbol": "AAPL",
        "side": "BUY",
        "order_type": "LIMIT",
        "quantity": "2.0000",
        "quote_price": "150.0000",
    }
    res = client.post("/api/v1/orders", json=payload_limit_buy, headers=headers)
    assert res.status_code == 201
    data = res.json()
    assert data["symbol"] == "AAPL"
    assert data["side"] == "BUY"
    assert data["order_type"] == "LIMIT"
    assert data["status"] == "PENDING"
    assert Decimal(data["quantity"]) == Decimal("2.0000")
    assert Decimal(data["quote_price"]) == Decimal("150.0000")
    assert "created_at" in data and data["created_at"] is not None

    # 2. MARKET BUY
    payload_market_buy = {
        "symbol": "GOOGL",
        "side": "BUY",
        "order_type": "MARKET",
        "quantity": "1.0000",
        "quote_price": "180.0000",
    }
    res = client.post("/api/v1/orders", json=payload_market_buy, headers=headers)
    assert res.status_code == 201
    assert res.json()["order_type"] == "MARKET"

    # 3. LIMIT SELL
    payload_limit_sell = {
        "symbol": "MSFT",
        "side": "SELL",
        "order_type": "LIMIT",
        "quantity": "5.0000",
        "quote_price": "400.0000",
    }
    res = client.post("/api/v1/orders", json=payload_limit_sell, headers=headers)
    assert res.status_code == 201
    assert res.json()["side"] == "SELL"

    # 4. MARKET SELL
    payload_market_sell = {
        "symbol": "AMZN",
        "side": "SELL",
        "order_type": "MARKET",
        "quantity": "3.0000",
        "quote_price": "185.0000",
    }
    res = client.post("/api/v1/orders", json=payload_market_sell, headers=headers)
    assert res.status_code == 201
    assert res.json()["order_type"] == "MARKET"


@pytest.mark.integration
@pytest.mark.ac("AC-07")
def test_ac_07_order_lifecycle_execution_and_immutability_api(db_session):
    """Verify AC-07: Pending order transitions to EXECUTED; modifying/cancelling EXECUTED order fails."""
    headers, customer = get_customer_auth_header(db_session, email="ac07_cust@marketscope.com")

    # Place order
    place_res = client.post(
        "/api/v1/orders",
        json={
            "symbol": "MSFT",
            "side": "BUY",
            "order_type": "LIMIT",
            "quantity": "1.0000",
            "quote_price": "300.0000",
        },
        headers=headers,
    )
    assert place_res.status_code == 201
    order_id = place_res.json()["id"]

    # Execute order
    exec_res = client.post(f"/api/v1/orders/{order_id}/execute", headers=headers)
    assert exec_res.status_code == 200
    assert exec_res.json()["status"] == "EXECUTED"

    # Attempt to cancel EXECUTED order must fail (AC-07, NFR-02)
    cancel_res = client.delete(f"/api/v1/orders/{order_id}", headers=headers)
    assert cancel_res.status_code == 400
    assert "invalid" in cancel_res.json()["detail"].lower() or "immutable" in cancel_res.json()["detail"].lower() or "cannot transition" in cancel_res.json()["detail"].lower()


@pytest.mark.integration
@pytest.mark.ac("AC-08")
def test_ac_08_insufficient_funds_validation_api(db_session):
    """Verify AC-08: BUY order exceeding customer available cash fails with InsufficientFundsException (400)."""
    headers, customer = get_customer_auth_header(db_session, email="ac08_cust@marketscope.com", available_cash=Decimal("500.0000"))

    # Required cost = 150.00 * 10 = 1500.00 > available 500.00
    payload = {
        "symbol": "AAPL",
        "side": "BUY",
        "order_type": "LIMIT",
        "quantity": "10.0000",
        "quote_price": "150.0000",
    }

    res = client.post("/api/v1/orders", json=payload, headers=headers)
    assert res.status_code == 400
    assert "insufficient funds" in res.json()["detail"].lower()


@pytest.mark.integration
def test_invalid_quantities_and_prices_api(db_session):
    """Verify order placement fails for non-positive quantities or prices."""
    headers, customer = get_customer_auth_header(db_session, email="invalid_qty_cust@marketscope.com")

    # Quantity <= 0
    res = client.post(
        "/api/v1/orders",
        json={"symbol": "AAPL", "side": "BUY", "order_type": "LIMIT", "quantity": "0.0000", "quote_price": "150.0000"},
        headers=headers,
    )
    assert res.status_code == 422  # Pydantic validation error gt=0

    # Price <= 0
    res = client.post(
        "/api/v1/orders",
        json={"symbol": "AAPL", "side": "BUY", "order_type": "LIMIT", "quantity": "1.0000", "quote_price": "-10.0000"},
        headers=headers,
    )
    assert res.status_code == 422


@pytest.mark.integration
def test_unauthorized_order_access_api(db_session):
    """Verify Customer A cannot cancel Customer B's order."""
    headers_a, cust_a = get_customer_auth_header(db_session, email="user_a@marketscope.com")
    headers_b, cust_b = get_customer_auth_header(db_session, email="user_b@marketscope.com")

    # User A places order
    place_res = client.post(
        "/api/v1/orders",
        json={"symbol": "TSLA", "side": "BUY", "order_type": "LIMIT", "quantity": "1.0000", "quote_price": "200.0000"},
        headers=headers_a,
    )
    assert place_res.status_code == 201
    order_id = place_res.json()["id"]

    # User B attempts to cancel User A's order -> 403 Forbidden
    cancel_res = client.delete(f"/api/v1/orders/{order_id}", headers=headers_b)
    assert cancel_res.status_code == 403


@pytest.mark.integration
def test_suspended_user_cannot_place_order_api(db_session):
    """Verify suspended user cannot access order placement endpoints."""
    headers, customer = get_customer_auth_header(db_session, email="suspended_trader@marketscope.com", state=AccountState.SUSPENDED)

    res = client.post(
        "/api/v1/orders",
        json={"symbol": "NVDA", "side": "BUY", "order_type": "LIMIT", "quantity": "1.0000", "quote_price": "100.0000"},
        headers=headers,
    )
    assert res.status_code == 403
    assert "suspended" in res.json()["detail"].lower()
