from src.domain.models import OrderStatus, OrderType, OrderSide
from src.domain.exceptions import InvalidOrderStateException


class OrderRules:
    """Business rules governing trade order placement and state transitions (AC-06, AC-07, NFR-02)."""

    ALLOWED_TRANSITIONS = {
        OrderStatus.PENDING: {OrderStatus.EXECUTED, OrderStatus.CANCELLED, OrderStatus.REJECTED},
        OrderStatus.EXECUTED: set(),   # Executed orders are append-only and immutable (NFR-02)
        OrderStatus.CANCELLED: set(),
        OrderStatus.REJECTED: set(),
    }

    @classmethod
    def validate_transition(cls, current_status: OrderStatus, new_status: OrderStatus) -> None:
        """Enforces PENDING -> EXECUTED / CANCELLED / REJECTED state machine (AC-07)."""
        valid_next_states = cls.ALLOWED_TRANSITIONS.get(current_status, set())
        if new_status not in valid_next_states:
            raise InvalidOrderStateException(
                f"Invalid order state transition from {current_status} to {new_status}."
            )

    @classmethod
    def enforce_executed_immutability(cls, status: OrderStatus) -> None:
        """Executed orders cannot be modified or deleted (NFR-02)."""
        if status == OrderStatus.EXECUTED:
            raise InvalidOrderStateException("Executed orders are immutable and cannot be updated.")
