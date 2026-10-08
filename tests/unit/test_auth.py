import pytest
from src.domain.models import UserRole, AccountState
from src.services.auth_service import AuthService
from src.services.user_service import UserService
from src.db.models import UserModel, AuditLogModel
from src.core.security import verify_password


@pytest.mark.unit
@pytest.mark.ac("AC-01")
def test_ac_01_customer_registration(db_session):
    """Verify AC-01: Customer registration creates account in ACTIVE state with role = CUSTOMER and bcrypt password hashing."""
    auth_service = AuthService(db_session)
    user = auth_service.register_customer("trader@marketscope.com", "SecurePass123!")

    assert user.id is not None
    assert user.email == "trader@marketscope.com"
    assert user.state == AccountState.ACTIVE
    assert user.role == UserRole.CUSTOMER
    # Verify password is stored as a valid bcrypt hash, not plaintext
    assert user.hashed_password != "SecurePass123!"
    assert verify_password("SecurePass123!", user.hashed_password) is True


@pytest.mark.unit
@pytest.mark.ac("AC-02")
def test_ac_02_admin_role_change(db_session):
    """Verify AC-02: Admin can change user roles and the action is audited with actor ID and server timestamp."""
    auth_service = AuthService(db_session)
    admin = auth_service.register_customer("admin@marketscope.com", "AdminPass123!")
    admin.role = UserRole.ADMIN
    db_session.commit()

    customer = auth_service.register_customer("customer@marketscope.com", "CustomerPass123!")

    user_service = UserService(db_session)
    updated_customer = user_service.update_user_role(
        actor=admin,
        target_user_id=customer.id,
        new_role=UserRole.SUSPENDED,
    )

    assert updated_customer.role == UserRole.SUSPENDED
    assert updated_customer.state == AccountState.SUSPENDED

    # Verify audit log entry
    audit = db_session.query(AuditLogModel).filter(AuditLogModel.target_user_id == customer.id).first()
    assert audit is not None
    assert audit.actor_id == admin.id
    assert audit.action == "UPDATE_USER_ROLE"
    assert "SUSPENDED" in audit.details
    assert audit.timestamp is not None
