from decimal import Decimal
import pytest
from src.domain.pnl_calculator import PnLCalculator


@pytest.mark.unit
@pytest.mark.ac("AC-09")
def test_ac_09_exact_portfolio_pnl_calculation():
    """Verify AC-09 exact spec example: 10 AAPL (buy 150, curr 180) + 5 MSFT (buy 300, curr 280)."""
    holdings = [
        {
            "symbol": "AAPL",
            "quantity": Decimal("10"),
            "average_buy_price": Decimal("150.00"),
            "current_price": Decimal("180.00"),
        },
        {
            "symbol": "MSFT",
            "quantity": Decimal("5"),
            "average_buy_price": Decimal("300.00"),
            "current_price": Decimal("280.00"),
        },
    ]

    stats = PnLCalculator.calculate_portfolio_stats(customer_id=101, holdings=holdings)

    assert isinstance(stats.total_invested, Decimal)
    assert stats.total_invested == Decimal("3000.00")
    assert stats.current_value == Decimal("3200.00")
    assert stats.absolute_pnl == Decimal("200.00")
    assert stats.percent_pnl == Decimal("6.67")


@pytest.mark.unit
def test_pnl_profit_and_loss_scenarios():
    """Verify PnL calculations for pure profit, pure loss, and net zero P&L."""
    # Profit scenario
    profit_holdings = [
        {"symbol": "NVDA", "quantity": Decimal("10"), "average_buy_price": Decimal("100.00"), "current_price": Decimal("150.00")}
    ]
    stats_profit = PnLCalculator.calculate_portfolio_stats(1, profit_holdings)
    assert stats_profit.absolute_pnl == Decimal("500.00")
    assert stats_profit.percent_pnl == Decimal("50.00")

    # Loss scenario
    loss_holdings = [
        {"symbol": "TSLA", "quantity": Decimal("10"), "average_buy_price": Decimal("200.00"), "current_price": Decimal("150.00")}
    ]
    stats_loss = PnLCalculator.calculate_portfolio_stats(1, loss_holdings)
    assert stats_loss.absolute_pnl == Decimal("-500.00")
    assert stats_loss.percent_pnl == Decimal("-25.00")

    # Zero P&L scenario
    zero_pnl_holdings = [
        {"symbol": "GOOGL", "quantity": Decimal("10"), "average_buy_price": Decimal("100.00"), "current_price": Decimal("100.00")}
    ]
    stats_zero = PnLCalculator.calculate_portfolio_stats(1, zero_pnl_holdings)
    assert stats_zero.absolute_pnl == Decimal("0.00")
    assert stats_zero.percent_pnl == Decimal("0.00")


@pytest.mark.unit
def test_pnl_zero_investment_scenario():
    """Verify customer with 0 holdings returns zero metrics without division by zero errors."""
    stats_empty = PnLCalculator.calculate_portfolio_stats(1, [])
    assert stats_empty.total_invested == Decimal("0.00")
    assert stats_empty.current_value == Decimal("0.00")
    assert stats_empty.absolute_pnl == Decimal("0.00")
    assert stats_empty.percent_pnl == Decimal("0.00")


@pytest.mark.unit
def test_pnl_fractional_quantities_and_precision():
    """Verify fractional share quantities and Decimal HALF_UP rounding precision."""
    fractional_holdings = [
        {"symbol": "BTC", "quantity": Decimal("1.2345"), "average_buy_price": Decimal("50000.1234"), "current_price": Decimal("55000.5678")}
    ]
    stats = PnLCalculator.calculate_portfolio_stats(1, fractional_holdings)
    assert isinstance(stats.total_invested, Decimal)
    assert isinstance(stats.percent_pnl, Decimal)


@pytest.mark.unit
def test_pnl_large_values():
    """Verify calculation correctness with large monetary values."""
    large_holdings = [
        {"symbol": "MEGA", "quantity": Decimal("1000000.0000"), "average_buy_price": Decimal("1000.0000"), "current_price": Decimal("1200.0000")}
    ]
    stats = PnLCalculator.calculate_portfolio_stats(1, large_holdings)
    assert stats.total_invested == Decimal("1000000000.00")
    assert stats.current_value == Decimal("1200000000.00")
    assert stats.absolute_pnl == Decimal("200000000.00")
    assert stats.percent_pnl == Decimal("20.00")


@pytest.mark.unit
def test_pnl_rejection_of_floats_and_invalid_negatives():
    """Verify float types raise TypeError and negative quantities/prices raise ValueError."""
    # Float type rejection (NFR-01)
    float_holdings = [
        {"symbol": "FAIL", "quantity": 10.5, "average_buy_price": Decimal("100.00"), "current_price": Decimal("110.00")}
    ]
    with pytest.raises(TypeError) as exc:
        PnLCalculator.calculate_portfolio_stats(1, float_holdings)
    assert "Decimal exclusively" in str(exc.value)

    # Negative values rejection
    negative_holdings = [
        {"symbol": "NEG", "quantity": Decimal("-5"), "average_buy_price": Decimal("100.00"), "current_price": Decimal("110.00")}
    ]
    with pytest.raises(ValueError) as exc_val:
        PnLCalculator.calculate_portfolio_stats(1, negative_holdings)
    assert "cannot be negative" in str(exc_val.value)
