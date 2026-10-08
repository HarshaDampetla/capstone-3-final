import pytest
from src.domain.watchlist_policy import WatchlistPolicy
from src.domain.exceptions import WatchlistUpdateException


@pytest.mark.unit
@pytest.mark.ac("AC-04")
def test_watchlist_count_limit():
    """Verify AC-04: Maximum 10 watchlists per customer enforced."""
    WatchlistPolicy.validate_watchlist_count(9)  # Allowed
    
    with pytest.raises(WatchlistUpdateException):
        WatchlistPolicy.validate_watchlist_count(10)  # Exception


@pytest.mark.unit
@pytest.mark.ac("AC-05")
def test_watchlist_atomic_symbol_cleaning():
    """Verify AC-05: Symbols list must not be empty and is cleaned atomically."""
    symbols = WatchlistPolicy.validate_atomic_symbols(["  aapl  ", "msft ", "AAPL"])
    assert symbols == ["AAPL", "MSFT"]

    with pytest.raises(WatchlistUpdateException):
        WatchlistPolicy.validate_atomic_symbols([])
