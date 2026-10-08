from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.db.models import UserModel
from src.api.dependencies import get_current_user
from src.api.schemas import OrderCreateRequest, OrderResponse
from src.services.order_service import OrderService
from src.domain.exceptions import InsufficientFundsException, InvalidOrderStateException, EntityNotFoundException, PermissionDeniedException

router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def place_order(
    request: OrderCreateRequest,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Places market or limit BUY/SELL trade order with cash validation (AC-06, AC-08)."""
    service = OrderService(db)
    try:
        order = service.place_order(
            user_id=current_user.id,
            symbol=request.symbol,
            side=request.side,
            order_type=request.order_type,
            quantity=request.quantity,
            quote_price=request.quote_price,
        )
        return order
    except (InsufficientFundsException, ValueError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("", response_model=List[OrderResponse])
def list_orders(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Lists trade orders for the current user."""
    service = OrderService(db)
    return service.get_user_orders(current_user.id)


@router.delete("/{order_id}", response_model=OrderResponse)
def cancel_order(
    order_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Cancels a pending order enforcing immutability rules (AC-07)."""
    service = OrderService(db)
    try:
        return service.cancel_order(order_id=order_id, user_id=current_user.id)
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionDeniedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except InvalidOrderStateException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{order_id}/execute", response_model=OrderResponse)
def execute_order(
    order_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Executes a pending trade order (AC-07)."""
    service = OrderService(db)
    try:
        return service.execute_order(order_id=order_id)
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidOrderStateException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except InsufficientFundsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
