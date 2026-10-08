from decimal import Decimal
from src.domain.models import OrderStatus, OrderSide, OrderType
from src.domain.exceptions import InvalidOrderStateException, InsufficientFundsException


class OrderPolicy:
    """Domain policy enforcing order state machine transitions and funds checks (AC-06, AC-07, AC-08)."""

    VALID_TRANSITIONS = {
        OrderStatus.PENDING: {OrderStatus.EXECUTED, OrderStatus.CANCELLED, OrderStatus.REJECTED},
        OrderStatus.EXECUTED: set(),   # Post-execution orders are append-only / immutable (NFR-02)
        OrderStatus.CANCELLED: set(),
        OrderStatus.REJECTED: set(),
    }

    @classmethod
    def validate_state_transition(cls, current_status: OrderStatus, new_status: OrderStatus) -> None:
        """Enforces PENDING -> EXECUTED / CANCELLED / REJECTED state machine (AC-07)."""
        allowed = cls.VALID_TRANSITIONS.get(current_status, set())
        if new_status not in allowed:
            raise InvalidOrderStateException(
                f"Cannot transition order from {current_status} to {new_status}."
            )

    @classmethod
    def validate_buy_order_funds(cls, quote_price: Decimal, quantity: Decimal, available_cash: Decimal) -> Decimal:
        """Validates BUY order total cost against customer available cash using Decimal (AC-08)."""
        if not isinstance(quote_price, Decimal) or not isinstance(quantity, Decimal) or not isinstance(available_cash, Decimal):
            raise TypeError("Financial calculations must use Python Decimal exclusively (NFR-01).")
        
        if quote_price <= Decimal("0") or quantity <= Decimal("0"):
            raise ValueError("Quote price and quantity must be strictly positive Decimal values.")

        total_cost = quote_price * quantity
        if total_cost > available_cash:
            raise InsufficientFundsException(
                f"Insufficient funds: Required {total_cost}, Available {available_cash}"
            )
        
        return total_cost
