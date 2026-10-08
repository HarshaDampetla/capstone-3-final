from decimal import Decimal
import pytest
from src.domain.models import OrderStatus
from src.domain.order_policy import OrderPolicy
from src.domain.exceptions import InvalidOrderStateException, InsufficientFundsException


@pytest.mark.unit
@pytest.mark.ac("AC-07")
def test_order_lifecycle_state_machine():
    """Verify AC-07: Order transition from PENDING to EXECUTED is valid, executed transitions raise exception."""
    OrderPolicy.validate_state_transition(OrderStatus.PENDING, OrderStatus.EXECUTED)
    OrderPolicy.validate_state_transition(OrderStatus.PENDING, OrderStatus.CANCELLED)

    with pytest.raises(InvalidOrderStateException):
        # Executed order is append-only / immutable (NFR-02)
        OrderPolicy.validate_state_transition(OrderStatus.EXECUTED, OrderStatus.PENDING)


@pytest.mark.unit
@pytest.mark.ac("AC-08")
def test_buy_order_insufficient_funds_exception():
    """Verify AC-08: BUY order raises InsufficientFundsException when total cost exceeds available cash."""
    quote_price = Decimal("150.00")
    quantity = Decimal("10")
    available_cash = Decimal("1000.00")  # Required = 1500.00

    with pytest.raises(InsufficientFundsException):
        OrderPolicy.validate_buy_order_funds(quote_price, quantity, available_cash)
        
    # Succeeds when cash is sufficient
    cost = OrderPolicy.validate_buy_order_funds(quote_price, quantity, Decimal("2000.00"))
    assert cost == Decimal("1500.00")
