from decimal import Decimal
import pytest
from src.domain.models import UserRole, AccountState, StockStatus
from src.domain.user_rules import UserRegistrationRules
from src.domain.role_rules import RoleManagementRules
from src.domain.stock_catalog_rules import StockCatalogRules
from src.domain.funds_validator import FundsValidator
from src.domain.portfolio_rules import PortfolioRules
from src.domain.exceptions import PermissionDeniedException, InsufficientFundsException


@pytest.mark.unit
@pytest.mark.ac("AC-01")
def test_user_registration_rules():
    UserRegistrationRules.validate_new_user("user@example.com", "Password123!")
    assert UserRegistrationRules.get_initial_account_state() == AccountState.ACTIVE
    assert UserRegistrationRules.get_initial_user_role() == UserRole.CUSTOMER

    with pytest.raises(ValueError):
        UserRegistrationRules.validate_new_user("invalid-email", "Password123!")


@pytest.mark.unit
@pytest.mark.ac("AC-02")
def test_role_management_rules():
    RoleManagementRules.validate_role_change(UserRole.ADMIN, UserRole.SUSPENDED)
    
    with pytest.raises(PermissionDeniedException):
        RoleManagementRules.validate_role_change(UserRole.CUSTOMER, UserRole.ADMIN)


@pytest.mark.unit
@pytest.mark.ac("AC-03")
def test_stock_catalog_rules():
    StockCatalogRules.validate_catalog_modification(UserRole.ADMIN)
    clean_sym = StockCatalogRules.validate_stock_creation("  nvda  ", Decimal("850.00"))
    assert clean_sym == "NVDA"
    assert StockCatalogRules.get_soft_deleted_status() == StockStatus.DELETED

    with pytest.raises(PermissionDeniedException):
        StockCatalogRules.validate_catalog_modification(UserRole.CUSTOMER)


@pytest.mark.unit
@pytest.mark.ac("AC-08")
def test_funds_validator_decimal_precision():
    cost = FundsValidator.validate_buy_order_cash(
        quote_price=Decimal("150.00"),
        quantity=Decimal("2"),
        available_cash=Decimal("500.00")
    )
    assert cost == Decimal("300.00")

    with pytest.raises(InsufficientFundsException):
        FundsValidator.validate_buy_order_cash(
            quote_price=Decimal("150.00"),
            quantity=Decimal("10"),
            available_cash=Decimal("500.00")
        )


@pytest.mark.unit
@pytest.mark.ac("AC-09")
def test_portfolio_rules_metrics():
    holdings = [
        {"quantity": Decimal("10"), "average_buy_price": Decimal("100.00"), "current_price": Decimal("150.00")}
    ]
    res = PortfolioRules.calculate_metrics(holdings)
    assert res["total_invested"] == Decimal("1000.00")
    assert res["current_value"] == Decimal("1500.00")
    assert res["absolute_pnl"] == Decimal("500.00")
    assert res["percent_pnl"] == Decimal("50.00")
