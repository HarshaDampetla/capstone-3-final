import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.core.security import create_access_token
from src.db.models import UserModel
from src.domain.models import UserRole, AccountState

client = TestClient(app)


@pytest.mark.integration
@pytest.mark.ac("AC-01")
def test_ac_01_customer_registration_api(db_session):
    """Verify AC-01 via API endpoint: Customer registration initializes ACTIVE state, CUSTOMER role, and bcrypt hash."""
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "newtrader@marketscope.com", "password": "Password123!"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newtrader@marketscope.com"
    assert data["state"] == "ACTIVE"
    assert data["role"] == "CUSTOMER"
    # Security requirement: password hash must NEVER be returned in response schema
    assert "password" not in data
    assert "hashed_password" not in data


@pytest.mark.integration
@pytest.mark.ac("AC-02")
def test_ac_02_admin_role_change_api(db_session):
    """Verify AC-02 via API endpoint: Admin role update sets target role and state."""
    admin = UserModel(email="admin_api@marketscope.com", hashed_password="hash", role=UserRole.ADMIN, state=AccountState.ACTIVE)
    customer = UserModel(email="cust_api@marketscope.com", hashed_password="hash", role=UserRole.CUSTOMER, state=AccountState.ACTIVE)
    db_session.add(admin)
    db_session.add(customer)
    db_session.commit()

    token = create_access_token(subject=admin.id, role=admin.role.value)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.put(
        f"/api/v1/admin/users/{customer.id}/role",
        headers=headers,
        json={"target_role": "SUSPENDED"}
    )
    assert response.status_code == 200
    assert response.json()["role"] == "SUSPENDED"
    assert response.json()["state"] == "SUSPENDED"


@pytest.mark.integration
def test_duplicate_registration_fails(db_session):
    """Verify duplicate email registration is rejected with HTTP 400."""
    user = UserModel(email="existing@marketscope.com", hashed_password="hash", role=UserRole.CUSTOMER, state=AccountState.ACTIVE)
    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/api/v1/auth/register",
        json={"email": "existing@marketscope.com", "password": "Password123!"}
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


@pytest.mark.integration
def test_customer_cannot_access_admin_endpoints(db_session):
    """Verify negative authorization: CUSTOMER role cannot access ADMIN endpoints (HTTP 403)."""
    customer = UserModel(email="cust_no_admin@marketscope.com", hashed_password="hash", role=UserRole.CUSTOMER, state=AccountState.ACTIVE)
    db_session.add(customer)
    db_session.commit()

    token = create_access_token(subject=customer.id, role=customer.role.value)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/v1/admin/users", headers=headers)
    assert response.status_code == 403
    assert "ADMIN role required" in response.json()["detail"]


@pytest.mark.integration
def test_suspended_user_cannot_access_protected_actions(db_session):
    """Verify negative authorization: SUSPENDED user is blocked from protected actions (HTTP 403)."""
    suspended = UserModel(email="suspended@marketscope.com", hashed_password="hash", role=UserRole.SUSPENDED, state=AccountState.SUSPENDED)
    db_session.add(suspended)
    db_session.commit()

    token = create_access_token(subject=suspended.id, role=suspended.role.value)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 403
    assert "suspended" in response.json()["detail"].lower()
