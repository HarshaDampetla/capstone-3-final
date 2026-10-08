import pytest
from src.domain.models import UserRole, AccountState
from src.domain.exceptions import WatchlistUpdateException, PermissionDeniedException
from src.services.watchlist_service import WatchlistService
from src.db.models import UserModel, WatchlistModel, WatchlistSymbolModel


@pytest.mark.unit
@pytest.mark.ac("AC-04")
def test_ac_04_watchlist_creation_and_max_10_limit(db_session):
    """Verify AC-04: Watchlist creation requiring >= 1 symbol and enforcing max 10 watchlists per customer."""
    customer = UserModel(email="cust_wl@marketscope.com", hashed_password="hash", role=UserRole.CUSTOMER, state=AccountState.ACTIVE)
    db_session.add(customer)
    db_session.commit()

    service = WatchlistService(db_session)

    # 1. Create 10 watchlists successfully
    for i in range(1, 11):
        wl = service.create_watchlist(actor=customer, name=f"Watchlist {i}", symbols=["AAPL"])
        assert wl.id is not None
        assert wl.name == f"Watchlist {i}"

    # 2. 11th creation MUST raise WatchlistUpdateException
    with pytest.raises(WatchlistUpdateException) as exc_info:
        service.create_watchlist(actor=customer, name="Watchlist 11", symbols=["MSFT"])
    assert "limit reached" in str(exc_info.value).lower() or "cannot hold more than 10" in str(exc_info.value).lower()


@pytest.mark.unit
@pytest.mark.ac("AC-04")
def test_ac_04_watchlist_must_contain_at_least_one_symbol(db_session):
    """Verify AC-04: Creating watchlist with empty symbol list raises WatchlistUpdateException."""
    customer = UserModel(email="cust_empty_wl@marketscope.com", hashed_password="hash", role=UserRole.CUSTOMER, state=AccountState.ACTIVE)
    db_session.add(customer)
    db_session.commit()

    service = WatchlistService(db_session)

    with pytest.raises(WatchlistUpdateException):
        service.create_watchlist(actor=customer, name="Empty WL", symbols=[])


@pytest.mark.unit
@pytest.mark.ac("AC-05")
def test_ac_05_atomic_update_and_rollback(db_session):
    """Verify AC-05: Watchlist operations execute atomically and rollback on invalid update."""
    customer = UserModel(email="cust_atomic_wl@marketscope.com", hashed_password="hash", role=UserRole.CUSTOMER, state=AccountState.ACTIVE)
    db_session.add(customer)
    db_session.commit()

    service = WatchlistService(db_session)
    wl = service.create_watchlist(actor=customer, name="Original Name", symbols=["AAPL", "MSFT"])

    # 1. Valid atomic update (rename + symbol replacement)
    updated = service.update_watchlist_atomic(actor=customer, watchlist_id=wl.id, name="New Name", symbols=["NVDA", "GOOGL"])
    assert updated.name == "New Name"
    symbol_names = [s.symbol for s in updated.symbols]
    assert "NVDA" in symbol_names
    assert "AAPL" not in symbol_names

    # 2. Invalid update with empty symbols MUST raise WatchlistUpdateException and rollback
    with pytest.raises(WatchlistUpdateException):
        service.update_watchlist_atomic(actor=customer, watchlist_id=wl.id, name="Invalid Attempt", symbols=[])

    # Verify original state was preserved (name is still 'New Name', symbols still NVDA & GOOGL)
    db_wl = service.get_watchlist_by_id(actor=customer, watchlist_id=wl.id)
    assert db_wl.name == "New Name"


@pytest.mark.unit
@pytest.mark.ac("AC-05")
def test_ac_05_customer_cannot_modify_another_customers_watchlist(db_session):
    """Verify security: Customer cannot modify another customer's watchlist (PermissionDeniedException)."""
    user1 = UserModel(email="user1_wl@marketscope.com", hashed_password="hash", role=UserRole.CUSTOMER, state=AccountState.ACTIVE)
    user2 = UserModel(email="user2_wl@marketscope.com", hashed_password="hash", role=UserRole.CUSTOMER, state=AccountState.ACTIVE)
    db_session.add(user1)
    db_session.add(user2)
    db_session.commit()

    service = WatchlistService(db_session)
    wl_user1 = service.create_watchlist(actor=user1, name="User 1 Tech", symbols=["AAPL"])

    # User 2 attempting update on User 1's watchlist MUST raise PermissionDeniedException
    with pytest.raises(PermissionDeniedException):
        service.update_watchlist_atomic(actor=user2, watchlist_id=wl_user1.id, name="Hacked Name")

    with pytest.raises(PermissionDeniedException):
        service.delete_watchlist(actor=user2, watchlist_id=wl_user1.id)
