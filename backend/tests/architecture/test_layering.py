import sys
import os
import ast
import inspect
import pytest


@pytest.mark.architecture
def test_domain_has_zero_external_layer_imports():
    """Rule 2: Domain layer must not import from API, Services, Repositories, or DB."""
    import src.domain.role_policy
    import src.domain.watchlist_policy
    import src.domain.order_policy
    import src.domain.pnl_calculator
    
    forbidden_prefixes = ("src.api", "src.services", "src.repositories", "src.db")
    
    for mod_name, mod in sys.modules.items():
        if mod_name.startswith("src.domain"):
            for attr_name in dir(mod):
                attr = getattr(mod, attr_name)
                if hasattr(attr, "__module__") and attr.__module__:
                    assert not any(attr.__module__.startswith(fp) for fp in forbidden_prefixes), (
                        f"Domain module {mod_name} illegally imports {attr.__module__}"
                    )


@pytest.mark.architecture
def test_controllers_do_not_import_repositories_directly():
    """Rule 1: API/Controllers layer must not import Repositories directly."""
    import src.api.health
    import src.api.schemas
    import src.api.order_router
    import src.api.portfolio_router
    
    for mod_name, mod in sys.modules.items():
        if mod_name.startswith("src.api"):
            for attr_name in dir(mod):
                attr = getattr(mod, attr_name)
                if hasattr(attr, "__module__") and attr.__module__:
                    assert not attr.__module__.startswith("src.repositories"), (
                        f"API module {mod_name} illegally imports Repository {attr.__module__}"
                    )


@pytest.mark.architecture
def test_repositories_do_not_import_controllers():
    """Rule 3: Repositories cannot depend on controllers/API layer."""
    import src.repositories.user_repository
    import src.repositories.catalog_repository
    import src.repositories.watchlist_repository
    import src.repositories.order_repository
    import src.repositories.portfolio_repository

    for mod_name, mod in sys.modules.items():
        if mod_name.startswith("src.repositories"):
            for attr_name in dir(mod):
                attr = getattr(mod, attr_name)
                if hasattr(attr, "__module__") and attr.__module__:
                    assert not attr.__module__.startswith("src.api"), (
                        f"Repository module {mod_name} illegally imports Controller {attr.__module__}"
                    )


@pytest.mark.architecture
def test_executed_orders_cannot_be_mutated():
    """Rule 4: Executed orders cannot be mutated (append-only immutability)."""
    from src.domain.models import OrderStatus
    from src.domain.order_policy import OrderPolicy
    from src.domain.order_rules import OrderRules
    from src.domain.exceptions import InvalidOrderStateException

    # Rejection of state mutation from EXECUTED
    with pytest.raises(InvalidOrderStateException):
        OrderPolicy.validate_state_transition(OrderStatus.EXECUTED, OrderStatus.PENDING)

    with pytest.raises(InvalidOrderStateException):
        OrderPolicy.validate_state_transition(OrderStatus.EXECUTED, OrderStatus.CANCELLED)

    with pytest.raises(InvalidOrderStateException):
        OrderRules.enforce_executed_immutability(OrderStatus.EXECUTED)


@pytest.mark.architecture
def test_admin_endpoints_require_admin_authorization():
    """Rule 5: ADMIN endpoints must include require_admin dependency."""
    from src.api.admin_user_router import router as admin_user_router
    from src.api.catalog_router import admin_router as admin_catalog_router
    from src.api.dependencies import require_admin

    for router in [admin_user_router, admin_catalog_router]:
        for route in router.routes:
            endpoint_fn = getattr(route, "endpoint", None)
            if endpoint_fn:
                sig = inspect.signature(endpoint_fn)
                # Check for require_admin in function default parameters
                has_admin_dep = any(
                    param.default is not inspect.Parameter.empty and hasattr(param.default, "dependency") and param.default.dependency == require_admin
                    for param in sig.parameters.values()
                )
                assert has_admin_dep, f"Admin endpoint {route.path} missing require_admin authorization check."


@pytest.mark.architecture
def test_financial_models_use_decimal_types():
    """Rule 6a: Domain financial entity fields must enforce Decimal types."""
    from decimal import Decimal
    from src.domain.models import CustomerBalance, PortfolioStats
    
    cb = CustomerBalance(customer_id=1, available_cash=Decimal("500.00"))
    assert isinstance(cb.available_cash, Decimal)
    
    with pytest.raises(TypeError):
        # Must reject float inputs for NFR-01 compliance
        CustomerBalance(customer_id=1, available_cash=500.00)  # type: ignore


@pytest.mark.architecture
def test_financial_calculations_never_use_float_ast():
    """Rule 6b: AST scan of domain financial files proves zero float usage."""
    financial_files = [
        "src/domain/pnl_calculator.py",
        "src/domain/funds_validator.py",
        "src/domain/order_policy.py",
    ]

    for rel_path in financial_files:
        full_path = os.path.abspath(rel_path)
        with open(full_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=full_path)

        for node in ast.walk(tree):
            # Check for float literal AST node (Constant of type float)
            if isinstance(node, ast.Constant) and isinstance(node.value, float):
                pytest.fail(f"Float literal {node.value} found in {rel_path} (Line {node.lineno})")
            # Check for call to float() function
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "float":
                pytest.fail(f"Illegal float() call found in {rel_path} (Line {node.lineno})")
