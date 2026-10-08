from typing import Optional, List
from decimal import Decimal
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from src.db.models import OrderModel, UserModel, PortfolioHoldingModel
from src.domain.models import OrderSide, OrderType, OrderStatus
from src.domain.exceptions import InvalidOrderStateException, InsufficientFundsException, EntityNotFoundException
from src.domain.order_rules import OrderRules
from src.domain.funds_validator import FundsValidator


class OrderRepository:
    """Repository managing Order and PortfolioHolding persistence (AC-06, AC-07, AC-08, NFR-02)."""

    def __init__(self, db: Session):
        self.db = db

    def create_order(
        self,
        user_id: int,
        symbol: str,
        side: OrderSide,
        order_type: OrderType,
        quantity: Decimal,
        quote_price: Decimal,
        status: OrderStatus = OrderStatus.PENDING,
    ) -> OrderModel:
        """Creates order in PENDING status with server-side timestamp (AC-06)."""
        order = OrderModel(
            user_id=user_id,
            symbol=symbol.upper(),
            side=side,
            order_type=order_type,
            quantity=quantity,
            quote_price=quote_price,
            status=status,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def get_order_by_id(self, order_id: int) -> Optional[OrderModel]:
        """Fetches order by primary key ID."""
        return self.db.query(OrderModel).filter(OrderModel.id == order_id).first()

    def get_user_orders(self, user_id: int) -> List[OrderModel]:
        """Lists all trade orders for a specific user."""
        return self.db.query(OrderModel).filter(OrderModel.user_id == user_id).order_by(OrderModel.created_at.desc()).all()

    def cancel_order(self, order_id: int, user_id: int) -> OrderModel:
        """Cancels a pending order enforcing immutability and state machine rules (AC-07)."""
        order = self.get_order_by_id(order_id)
        if not order:
            raise EntityNotFoundException(f"Order with ID {order_id} not found.")

        # Enforce state machine transition PENDING -> CANCELLED (AC-07)
        OrderRules.validate_transition(order.status, OrderStatus.CANCELLED)

        order.status = OrderStatus.CANCELLED
        order.updated_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(order)
        return order

    def execute_order(self, order_id: int) -> OrderModel:
        """Executes a pending order, updating user cash and portfolio holdings atomically (AC-07, AC-08)."""
        order = self.get_order_by_id(order_id)
        if not order:
            raise EntityNotFoundException(f"Order with ID {order_id} not found.")

        # Validate state machine (AC-07)
        OrderRules.validate_transition(order.status, OrderStatus.EXECUTED)

        user = self.db.query(UserModel).filter(UserModel.id == order.user_id).first()
        if not user:
            raise EntityNotFoundException(f"User with ID {order.user_id} not found.")

        try:
            if order.side == OrderSide.BUY:
                total_cost = FundsValidator.validate_buy_order_cash(order.quote_price, order.quantity, user.available_cash)
                user.available_cash -= total_cost

                # Update or create portfolio holding
                holding = (
                    self.db.query(PortfolioHoldingModel)
                    .filter(PortfolioHoldingModel.user_id == user.id, PortfolioHoldingModel.symbol == order.symbol)
                    .first()
                )
                if holding:
                    current_cost_basis = holding.quantity * holding.average_buy_price
                    new_quantity = holding.quantity + order.quantity
                    new_cost_basis = current_cost_basis + total_cost
                    holding.average_buy_price = new_cost_basis / new_quantity
                    holding.quantity = new_quantity
                else:
                    new_holding = PortfolioHoldingModel(
                        user_id=user.id,
                        symbol=order.symbol,
                        quantity=order.quantity,
                        average_buy_price=order.quote_price,
                    )
                    self.db.add(new_holding)

            elif order.side == OrderSide.SELL:
                total_proceeds = order.quote_price * order.quantity
                user.available_cash += total_proceeds

                holding = (
                    self.db.query(PortfolioHoldingModel)
                    .filter(PortfolioHoldingModel.user_id == user.id, PortfolioHoldingModel.symbol == order.symbol)
                    .first()
                )
                if holding:
                    holding.quantity -= order.quantity
                    if holding.quantity <= Decimal("0"):
                        self.db.delete(holding)

            order.status = OrderStatus.EXECUTED
            order.updated_at = datetime.now(timezone.utc)
            self.db.commit()
            self.db.refresh(order)
            return order
        except Exception:
            self.db.rollback()
            raise
