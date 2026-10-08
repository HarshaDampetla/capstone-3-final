class DomainException(Exception):
    """Base exception for all domain business rule violations."""
    pass


class WatchlistUpdateException(DomainException):
    """Raised when atomic watchlist operation fails or exceeds limits (AC-05)."""
    pass


class InvalidOrderStateException(DomainException):
    """Raised when illegal order state transition is attempted (AC-07)."""
    pass


class InsufficientFundsException(DomainException):
    """Raised when BUY order total cost exceeds customer available cash (AC-08)."""
    pass


class EntityNotFoundException(DomainException):
    """Raised when requested entity is missing."""
    pass


class PermissionDeniedException(DomainException):
    """Raised when actor role is unauthorized for requested operation."""
    pass
