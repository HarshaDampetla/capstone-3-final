from typing import List
from src.domain.exceptions import WatchlistUpdateException


class WatchlistRules:
    """Business rules governing customer watchlists (AC-04, AC-05)."""

    MAX_WATCHLISTS_PER_CUSTOMER = 10

    @classmethod
    def enforce_watchlist_limit(cls, current_watchlist_count: int) -> None:
        """Customer may hold a maximum of 10 watchlists (AC-04)."""
        if current_watchlist_count >= cls.MAX_WATCHLISTS_PER_CUSTOMER:
            raise WatchlistUpdateException(
                f"Watchlist creation limit reached: customer cannot hold more than {cls.MAX_WATCHLISTS_PER_CUSTOMER} watchlists."
            )

    @classmethod
    def validate_atomic_creation(cls, name: str, symbols: List[str]) -> None:
        """Watchlist creation requires a non-empty name and at least 1 symbol (AC-04)."""
        if not name or not name.strip():
            raise WatchlistUpdateException("Watchlist name cannot be empty.")
        if not symbols or len(symbols) == 0:
            raise WatchlistUpdateException("Watchlist must contain at least one symbol.")

    @classmethod
    def validate_atomic_symbol_list(cls, symbols: List[str]) -> List[str]:
        """Validates and cleans symbol list atomically (AC-05)."""
        if not symbols or len(symbols) == 0:
            raise WatchlistUpdateException("Atomic symbol update failed: symbol list cannot be empty.")
        
        cleaned = [s.strip().upper() for s in symbols if s and s.strip()]
        if len(cleaned) == 0:
            raise WatchlistUpdateException("Atomic symbol update failed: no valid symbols provided.")
        
        return list(dict.fromkeys(cleaned))
