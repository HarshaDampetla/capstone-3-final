from decimal import Decimal
from typing import Optional, List
from sqlalchemy.orm import Session
from src.db.models import StockCatalogModel, AuditLogModel
from src.domain.models import StockStatus


class CatalogRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_symbol(self, symbol: str) -> Optional[StockCatalogModel]:
        return self.db.query(StockCatalogModel).filter(
            StockCatalogModel.symbol == symbol.upper()
        ).first()

    def create_symbol(
        self,
        symbol: str,
        company_name: str,
        sector: str,
        exchange: str,
        current_price: Decimal,
        actor_id: Optional[int] = None,
    ) -> StockCatalogModel:
        stock = StockCatalogModel(
            symbol=symbol.upper(),
            company_name=company_name,
            sector=sector,
            exchange=exchange,
            current_price=current_price,
            status=StockStatus.ACTIVE,
        )
        self.db.add(stock)
        
        if actor_id:
            audit = AuditLogModel(
                actor_id=actor_id,
                action="CREATE_STOCK_SYMBOL",
                details=f"Created symbol {symbol.upper()} with price {current_price}",
            )
            self.db.add(audit)
            
        self.db.commit()
        self.db.refresh(stock)
        return stock

    def update_symbol(
        self,
        symbol: str,
        company_name: Optional[str] = None,
        sector: Optional[str] = None,
        exchange: Optional[str] = None,
        current_price: Optional[Decimal] = None,
        actor_id: Optional[int] = None,
    ) -> Optional[StockCatalogModel]:
        stock = self.get_by_symbol(symbol)
        if not stock:
            return None

        if company_name:
            stock.company_name = company_name
        if sector:
            stock.sector = sector
        if exchange:
            stock.exchange = exchange
        if current_price is not None:
            stock.current_price = current_price

        if actor_id:
            audit = AuditLogModel(
                actor_id=actor_id,
                action="UPDATE_STOCK_SYMBOL",
                details=f"Updated symbol {stock.symbol}",
            )
            self.db.add(audit)

        self.db.commit()
        self.db.refresh(stock)
        return stock

    def soft_delete_symbol(self, symbol: str, actor_id: Optional[int] = None) -> Optional[StockCatalogModel]:
        """Soft-delete moves symbol to DELETED status — symbols are never hard-deleted (AC-03)."""
        stock = self.get_by_symbol(symbol)
        if not stock:
            return None

        stock.status = StockStatus.DELETED
        
        if actor_id:
            audit = AuditLogModel(
                actor_id=actor_id,
                action="SOFT_DELETE_STOCK_SYMBOL",
                details=f"Soft-deleted symbol {stock.symbol} to DELETED state",
            )
            self.db.add(audit)

        self.db.commit()
        self.db.refresh(stock)
        return stock

    def search_stocks(
        self,
        symbol: Optional[str] = None,
        sector: Optional[str] = None,
        exchange: Optional[str] = None,
        include_deleted: bool = False,
    ) -> List[StockCatalogModel]:
        query = self.db.query(StockCatalogModel)

        if not include_deleted:
            query = query.filter(StockCatalogModel.status == StockStatus.ACTIVE)

        if symbol:
            query = query.filter(StockCatalogModel.symbol.like(f"%{symbol.upper()}%"))
        if sector:
            query = query.filter(StockCatalogModel.sector.ilike(f"%{sector}%"))
        if exchange:
            query = query.filter(StockCatalogModel.exchange.ilike(f"%{exchange}%"))

        return query.all()
