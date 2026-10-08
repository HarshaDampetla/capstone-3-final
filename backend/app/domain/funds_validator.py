from decimal import Decimal
from src.domain.exceptions import InsufficientFundsException


class FundsValidator:
    """Business rules validating available customer cash for BUY orders using Python Decimal (AC-08, NFR-01)."""

    @classmethod
    def validate_buy_order_cash(
        cls,
        quote_price: Decimal,
        quantity: Decimal,
        available_cash: Decimal
    ) -> Decimal:
        """Validates BUY order total cost against available cash (AC-08)."""
        if not isinstance(quote_price, Decimal) or not isinstance(quantity, Decimal) or not isinstance(available_cash, Decimal):
            raise TypeError("Financial values must use Python Decimal exclusively (NFR-01).")

        if quote_price <= Decimal("0") or quantity <= Decimal("0"):
            raise ValueError("Quote price and quantity must be strictly positive Decimal values.")

        total_cost = quote_price * quantity
        if total_cost > available_cash:
            raise InsufficientFundsException(
                f"Insufficient funds: BUY order total cost {total_cost} exceeds available cash {available_cash}."
            )

        return total_cost
