from typing import List, Optional
from decimal import Decimal
from sqlalchemy.orm import Session
from src.db.models import OrderModel, UserModel
from src.domain.models import OrderSide, OrderType, OrderStatus
from src.domain.exceptions import InsufficientFundsException, InvalidOrderStateException, EntityNotFoundException, PermissionDeniedException
from src.domain.funds_validator import FundsValidator
from src.repositories.order_repository import OrderRepository
from src.repositories.user_repository import UserRepository


class OrderService:
    """Service layer executing trade order business logic (AC-06, AC-07, AC-08)."""

    def __init__(self, db: Session):
        self.db = db
        self.order_repo = OrderRepository(db)
        self.user_repo = UserRepository(db)

    def place_order(
        self,
        user_id: int,
        symbol: str,
        side: OrderSide,
        order_type: OrderType,
        quantity: Decimal,
        quote_price: Decimal,
    ) -> OrderModel:
        """Places a market or limit trade order in PENDING status with funds validation (AC-06, AC-08)."""
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise EntityNotFoundException(f"User with ID {user_id} not found.")

        if quantity <= Decimal("0") or quote_price <= Decimal("0"):
            raise ValueError("Quantity and quote price must be strictly positive Decimal values.")

        # Validate funds for BUY orders using Decimal arithmetic (AC-08, NFR-01)
        if side == OrderSide.BUY:
            FundsValidator.validate_buy_order_cash(quote_price, quantity, user.available_cash)

        # Create order in PENDING state with server timestamp (AC-06)
        return self.order_repo.create_order(
            user_id=user_id,
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            quote_price=quote_price,
            status=OrderStatus.PENDING,
        )

    def get_user_orders(self, user_id: int) -> List[OrderModel]:
        """Lists trade orders for the specified user."""
        return self.order_repo.get_user_orders(user_id)

    def cancel_order(self, order_id: int, user_id: int) -> OrderModel:
        """Cancels a pending trade order enforcing user authorization and immutability (AC-07)."""
        order = self.order_repo.get_order_by_id(order_id)
        if not order:
            raise EntityNotFoundException(f"Order with ID {order_id} not found.")

        if order.user_id != user_id:
            raise PermissionDeniedException("You can only cancel your own trade orders.")

        return self.order_repo.cancel_order(order_id=order_id, user_id=user_id)

    def execute_order(self, order_id: int) -> OrderModel:
        """Executes a pending order and updates cash/holdings atomically (AC-07)."""
        return self.order_repo.execute_order(order_id=order_id)
