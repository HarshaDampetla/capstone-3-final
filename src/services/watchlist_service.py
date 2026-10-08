from typing import Optional, List
from sqlalchemy.orm import Session
from src.db.models import WatchlistModel, UserModel
from src.domain.watchlist_rules import WatchlistRules
from src.domain.exceptions import WatchlistUpdateException, PermissionDeniedException
from src.repositories.watchlist_repository import WatchlistRepository


class WatchlistService:
    def __init__(self, db: Session):
        self.repo = WatchlistRepository(db)

    def create_watchlist(self, actor: UserModel, name: str, symbols: List[str]) -> WatchlistModel:
        """Customer operation: create watchlist (AC-04)."""
        # Enforce max 10 watchlists per customer
        current_count = self.repo.count_customer_watchlists(actor.id)
        WatchlistRules.enforce_watchlist_limit(current_count)

        # Validate creation attributes
        WatchlistRules.validate_atomic_creation(name, symbols)
        clean_symbols = WatchlistRules.validate_atomic_symbol_list(symbols)

        return self.repo.create_watchlist(user_id=actor.id, name=name, symbols=clean_symbols)

    def get_customer_watchlists(self, actor: UserModel) -> List[WatchlistModel]:
        """List watchlists belonging to authenticated customer."""
        return self.repo.get_customer_watchlists(actor.id)

    def get_watchlist_by_id(self, actor: UserModel, watchlist_id: int) -> WatchlistModel:
        """Get specific watchlist with ownership validation."""
        watchlist = self.repo.get_by_id(watchlist_id)
        if not watchlist:
            raise WatchlistUpdateException(f"Watchlist with ID {watchlist_id} not found.")

        if watchlist.user_id != actor.id:
            raise PermissionDeniedException("Cannot access another customer's watchlist.")

        return watchlist

    def update_watchlist_atomic(
        self,
        actor: UserModel,
        watchlist_id: int,
        name: Optional[str] = None,
        symbols: Optional[List[str]] = None,
    ) -> WatchlistModel:
        """Atomically update watchlist name or symbols (AC-05)."""
        # Validate ownership
        self.get_watchlist_by_id(actor, watchlist_id)

        clean_symbols = None
        if symbols is not None:
            clean_symbols = WatchlistRules.validate_atomic_symbol_list(symbols)

        return self.repo.update_watchlist_atomic(
            watchlist_id=watchlist_id,
            name=name,
            symbols=clean_symbols,
        )

    def delete_watchlist(self, actor: UserModel, watchlist_id: int) -> None:
        """Delete watchlist (AC-05)."""
        # Validate ownership
        self.get_watchlist_by_id(actor, watchlist_id)
        self.repo.delete_watchlist(watchlist_id)
