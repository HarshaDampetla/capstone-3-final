from decimal import Decimal
from typing import Optional, List
from sqlalchemy.orm import Session
from src.db.models import StockCatalogModel, UserModel
from src.domain.models import StockStatus
from src.domain.stock_catalog_rules import StockCatalogRules
from src.repositories.catalog_repository import CatalogRepository


class CatalogService:
    def __init__(self, db: Session):
        self.catalog_repo = CatalogRepository(db)

    def create_stock(
        self,
        actor: UserModel,
        symbol: str,
        company_name: str,
        sector: str,
        exchange: str,
        current_price: Decimal,
    ) -> StockCatalogModel:
        """Admin operation: create stock symbol (AC-03)."""
        StockCatalogRules.validate_catalog_modification(actor.role)
        clean_symbol = StockCatalogRules.validate_stock_creation(symbol, current_price)

        existing = self.catalog_repo.get_by_symbol(clean_symbol)
        if existing:
            raise ValueError(f"Stock symbol '{clean_symbol}' already exists in catalog.")

        return self.catalog_repo.create_symbol(
            symbol=clean_symbol,
            company_name=company_name,
            sector=sector,
            exchange=exchange,
            current_price=current_price,
            actor_id=actor.id,
        )

    def update_stock(
        self,
        actor: UserModel,
        symbol: str,
        company_name: Optional[str] = None,
        sector: Optional[str] = None,
        exchange: Optional[str] = None,
        current_price: Optional[Decimal] = None,
    ) -> StockCatalogModel:
        """Admin operation: update stock details (AC-03)."""
        StockCatalogRules.validate_catalog_modification(actor.role)
        if current_price is not None:
            StockCatalogRules.validate_stock_creation(symbol, current_price)

        updated = self.catalog_repo.update_symbol(
            symbol=symbol,
            company_name=company_name,
            sector=sector,
            exchange=exchange,
            current_price=current_price,
            actor_id=actor.id,
        )
        if not updated:
            raise ValueError(f"Stock symbol '{symbol}' not found.")
        return updated

    def soft_delete_stock(self, actor: UserModel, symbol: str) -> StockCatalogModel:
        """Admin operation: soft-delete stock symbol (AC-03)."""
        StockCatalogRules.validate_catalog_modification(actor.role)
        deleted = self.catalog_repo.soft_delete_symbol(symbol=symbol, actor_id=actor.id)
        if not deleted:
            raise ValueError(f"Stock symbol '{symbol}' not found.")
        return deleted

    def search_stocks(
        self,
        symbol: Optional[str] = None,
        sector: Optional[str] = None,
        exchange: Optional[str] = None,
    ) -> List[StockCatalogModel]:
        """Browse active stock catalog with optional symbol/sector/exchange filters (AC-03)."""
        return self.catalog_repo.search_stocks(
            symbol=symbol,
            sector=sector,
            exchange=exchange,
            include_deleted=False,
        )

    def get_stock_by_symbol(self, symbol: str) -> StockCatalogModel:
        stock = self.catalog_repo.get_by_symbol(symbol)
        if not stock:
            raise ValueError(f"Stock symbol '{symbol}' not found.")
        return stock
