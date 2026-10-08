from decimal import Decimal
from src.domain.models import StockStatus, UserRole
from src.domain.exceptions import PermissionDeniedException


class StockCatalogRules:
    """Business rules governing stock catalog CRUD and soft deletion (AC-03)."""

    @classmethod
    def validate_catalog_modification(cls, actor_role: UserRole) -> None:
        """Catalog CRUD operations are restricted to ADMIN role only (AC-03)."""
        if actor_role != UserRole.ADMIN:
            raise PermissionDeniedException("Only ADMIN users can perform stock catalog modifications.")

    @classmethod
    def validate_stock_creation(cls, symbol: str, price: Decimal) -> str:
        """Validates symbol uppercase formatting and strictly positive Decimal price."""
        if not symbol or not symbol.strip():
            raise ValueError("Stock symbol cannot be empty.")
        if not isinstance(price, Decimal) or price <= Decimal("0"):
            raise ValueError("Stock price must be a strictly positive Decimal value.")
        return symbol.strip().upper()

    @classmethod
    def get_soft_deleted_status(cls) -> StockStatus:
        """Soft-delete moves symbol to DELETED status — symbols are never hard-deleted (AC-03)."""
        return StockStatus.DELETED
