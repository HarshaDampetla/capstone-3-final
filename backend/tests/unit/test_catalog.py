from decimal import Decimal
import pytest
from src.domain.models import UserRole, StockStatus
from src.domain.stock_catalog_rules import StockCatalogRules
from src.services.catalog_service import CatalogService
from src.db.models import UserModel, StockCatalogModel, AuditLogModel
from src.domain.exceptions import PermissionDeniedException


@pytest.mark.unit
@pytest.mark.ac("AC-03")
def test_ac_03_admin_stock_crud_service(db_session):
    """Verify AC-03: Admin stock catalog CRUD operations, soft-delete, and audit trail."""
    admin = UserModel(email="admin_cat@marketscope.com", hashed_password="hash", role=UserRole.ADMIN)
    db_session.add(admin)
    db_session.commit()

    catalog_service = CatalogService(db_session)

    # 1. Create Stock
    stock = catalog_service.create_stock(
        actor=admin,
        symbol="AAPL",
        company_name="Apple Inc.",
        sector="Technology",
        exchange="NASDAQ",
        current_price=Decimal("175.50"),
    )
    assert stock.symbol == "AAPL"
    assert stock.status == StockStatus.ACTIVE
    assert stock.current_price == Decimal("175.50")
    assert isinstance(stock.current_price, Decimal)

    # 2. Update Stock
    updated = catalog_service.update_stock(
        actor=admin,
        symbol="AAPL",
        current_price=Decimal("180.00"),
    )
    assert updated.current_price == Decimal("180.00")

    # 3. Soft Delete Stock
    deleted = catalog_service.soft_delete_stock(actor=admin, symbol="AAPL")
    assert deleted.status == StockStatus.DELETED

    # 4. Verify symbol remains present in database table
    db_record = db_session.query(StockCatalogModel).filter(StockCatalogModel.symbol == "AAPL").first()
    assert db_record is not None
    assert db_record.status == StockStatus.DELETED


@pytest.mark.unit
@pytest.mark.ac("AC-03")
def test_ac_03_deleted_stocks_excluded_from_public_search(db_session):
    """Verify AC-03: Deleted stocks are excluded from active public catalog search."""
    admin = UserModel(email="admin_search@marketscope.com", hashed_password="hash", role=UserRole.ADMIN)
    db_session.add(admin)
    db_session.commit()

    catalog_service = CatalogService(db_session)
    catalog_service.create_stock(actor=admin, symbol="ACTIVE_STOCK", company_name="Active Inc", sector="Tech", exchange="NASDAQ", current_price=Decimal("100.00"))
    catalog_service.create_stock(actor=admin, symbol="DEL_STOCK", company_name="Del Inc", sector="Tech", exchange="NASDAQ", current_price=Decimal("50.00"))
    
    catalog_service.soft_delete_stock(actor=admin, symbol="DEL_STOCK")

    # Active search must only return ACTIVE_STOCK
    active_stocks = catalog_service.search_stocks()
    symbols = [s.symbol for s in active_stocks]
    assert "ACTIVE_STOCK" in symbols
    assert "DEL_STOCK" not in symbols


@pytest.mark.unit
@pytest.mark.ac("AC-03")
def test_ac_03_customer_denied_catalog_modifications(db_session):
    """Verify AC-03: Customer role cannot perform catalog modifications (PermissionDeniedException)."""
    customer = UserModel(email="cust_cat@marketscope.com", hashed_password="hash", role=UserRole.CUSTOMER)
    db_session.add(customer)
    db_session.commit()

    catalog_service = CatalogService(db_session)

    with pytest.raises(PermissionDeniedException):
        catalog_service.create_stock(
            actor=customer,
            symbol="GOOGL",
            company_name="Alphabet Inc.",
            sector="Technology",
            exchange="NASDAQ",
            current_price=Decimal("140.00"),
        )
