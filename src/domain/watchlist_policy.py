from typing import List
from src.domain.exceptions import WatchlistUpdateException


class WatchlistPolicy:
    """Domain policy enforcing watchlist limits and atomic update invariants (AC-04, AC-05)."""

    MAX_WATCHLISTS_PER_CUSTOMER = 10

    @classmethod
    def validate_watchlist_count(cls, current_count: int) -> None:
        """Enforces maximum 10 watchlists per customer (AC-04)."""
        if current_count >= cls.MAX_WATCHLISTS_PER_CUSTOMER:
            raise WatchlistUpdateException(
                f"Customer cannot hold more than {cls.MAX_WATCHLISTS_PER_CUSTOMER} watchlists."
            )

    @classmethod
    def validate_watchlist_creation(cls, name: str, symbols: List[str]) -> None:
        """Validates watchlist creation parameters (name non-empty, at least 1 symbol)."""
        if not name or not name.strip():
            raise WatchlistUpdateException("Watchlist name cannot be empty.")
        
        if not symbols or len(symbols) == 0:
            raise WatchlistUpdateException("Watchlist must contain at least one symbol.")

    @classmethod
    def validate_atomic_symbols(cls, symbols: List[str]) -> List[str]:
        """Validates and deduplicates symbol list atomically (AC-05)."""
        if not symbols:
            raise WatchlistUpdateException("Watchlist symbols list cannot be empty.")
        
        clean_symbols = [s.strip().upper() for s in symbols if s and s.strip()]
        if len(clean_symbols) == 0:
            raise WatchlistUpdateException("Invalid symbols provided for watchlist.")
        
        return list(dict.fromkeys(clean_symbols))
