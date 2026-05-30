"""Repository layer - Data access abstraction."""
from repositories.base_repository import BaseRepository
from repositories.book_repository import BookRepository
from repositories.book_status_repository import BookStatusRepository
from repositories.review_repository import ReviewRepository
from repositories.tbr_repository import TBRRepository
from repositories.stats_repository import StatsRepository

__all__ = [
    "BaseRepository",
    "BookRepository",
    "BookStatusRepository",
    "ReviewRepository",
    "TBRRepository",
    "StatsRepository",
]
