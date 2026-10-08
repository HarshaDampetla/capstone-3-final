from typing import Optional, List
from sqlalchemy.orm import Session
from src.db.models import WatchlistModel, WatchlistSymbolModel
from src.domain.exceptions import WatchlistUpdateException


class WatchlistRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, watchlist_id: int) -> Optional[WatchlistModel]:
        return self.db.query(WatchlistModel).filter(WatchlistModel.id == watchlist_id).first()

    def get_customer_watchlists(self, user_id: int) -> List[WatchlistModel]:
        return self.db.query(WatchlistModel).filter(WatchlistModel.user_id == user_id).all()

    def count_customer_watchlists(self, user_id: int) -> int:
        return self.db.query(WatchlistModel).filter(WatchlistModel.user_id == user_id).count()

    def create_watchlist(self, user_id: int, name: str, symbols: List[str]) -> WatchlistModel:
        """Atomic creation of watchlist with symbols (AC-04, AC-05)."""
        try:
            watchlist = WatchlistModel(user_id=user_id, name=name)
            self.db.add(watchlist)
            self.db.flush()  # assign watchlist.id

            for sym in symbols:
                sym_model = WatchlistSymbolModel(watchlist_id=watchlist.id, symbol=sym.upper())
                self.db.add(sym_model)

            self.db.commit()
            self.db.refresh(watchlist)
            return watchlist
        except Exception as e:
            self.db.rollback()
            raise WatchlistUpdateException(f"Failed to create watchlist atomically: {str(e)}")

    def update_watchlist_atomic(
        self,
        watchlist_id: int,
        name: Optional[str] = None,
        symbols: Optional[List[str]] = None,
    ) -> WatchlistModel:
        """Atomic update of name and symbol list (AC-05)."""
        watchlist = self.get_by_id(watchlist_id)
        if not watchlist:
            raise WatchlistUpdateException(f"Watchlist with ID {watchlist_id} not found.")

        try:
            if name:
                watchlist.name = name

            if symbols is not None:
                # Remove existing symbols
                self.db.query(WatchlistSymbolModel).filter(
                    WatchlistSymbolModel.watchlist_id == watchlist_id
                ).delete()

                # Add new symbols
                for sym in symbols:
                    sym_model = WatchlistSymbolModel(watchlist_id=watchlist_id, symbol=sym.upper())
                    self.db.add(sym_model)

            self.db.commit()
            self.db.refresh(watchlist)
            return watchlist
        except WatchlistUpdateException:
            self.db.rollback()
            raise
        except Exception as e:
            self.db.rollback()
            raise WatchlistUpdateException(f"Atomic update failed and was rolled back: {str(e)}")

    def delete_watchlist(self, watchlist_id: int) -> None:
        """Atomic deletion of watchlist and its associated symbols (AC-05)."""
        watchlist = self.get_by_id(watchlist_id)
        if not watchlist:
            raise WatchlistUpdateException(f"Watchlist with ID {watchlist_id} not found.")

        try:
            self.db.delete(watchlist)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise WatchlistUpdateException(f"Atomic deletion failed: {str(e)}")
