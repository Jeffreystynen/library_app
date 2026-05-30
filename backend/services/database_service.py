"""Database Service - Abstracts repository access with business logic."""
from repositories.book_repository import BookRepository
from repositories.book_status_repository import BookStatusRepository
from repositories.review_repository import ReviewRepository
from repositories.tbr_repository import TBRRepository
from repositories.stats_repository import StatsRepository
from utils.validators import (
    validate_book_data,
    validate_status_update,
    validate_rating_update,
    validate_progress_update,
    validate_review_data,
)
from utils.constants import ErrorMessages, BookStatus


class DatabaseService:
    """Service layer for database operations with business logic."""

    def __init__(self):
        """Initialize service with all repositories."""
        self.book_repo = BookRepository()
        self.status_repo = BookStatusRepository()
        self.review_repo = ReviewRepository()
        self.tbr_repo = TBRRepository()
        self.stats_repo = StatsRepository()

    # ==================== BOOK OPERATIONS ====================

    def get_book(self, book_id):
        """Get a single book by ID."""
        book = self.book_repo.find_by_id(book_id)
        if not book:
            raise ValueError(ErrorMessages.BOOK_NOT_FOUND)
        return book

    def list_books(self, limit=20, offset=0, status=None, genre=None, sort_by="title"):
        """List all books with filtering and pagination."""
        return self.book_repo.find_all(limit, offset, status, genre, sort_by)

    def search_books(self, search_term, limit=50):
        """Search books by title, author, or genre."""
        if not search_term or len(search_term) < 2:
            raise ValueError("Search term must be at least 2 characters")
        return self.book_repo.search(search_term, limit)

    def create_book(self, title, author_id, **kwargs):
        """Create a new book with validation."""
        data = {"title": title, "author_id": author_id, **kwargs}
        errors = validate_book_data(data)
        if errors is not True:
            raise ValueError(f"Validation failed: {errors}")

        return self.book_repo.create(
            title=title,
            author_id=author_id,
            isbn=kwargs.get("isbn"),
            publication_year=kwargs.get("publication_year"),
            genre=kwargs.get("genre"),
            description=kwargs.get("description"),
            cover_url=kwargs.get("cover_url"),
            pages=kwargs.get("pages"),
        )

    def update_book(self, book_id, **kwargs):
        """Update book information."""
        if not self.book_repo.exists(book_id):
            raise ValueError(ErrorMessages.BOOK_NOT_FOUND)

        errors = validate_book_data(kwargs)
        if errors is not True:
            raise ValueError(f"Validation failed: {errors}")

        return self.book_repo.update(book_id, **kwargs)

    def delete_book(self, book_id):
        """Delete a book."""
        if not self.book_repo.exists(book_id):
            raise ValueError(ErrorMessages.BOOK_NOT_FOUND)
        return self.book_repo.delete(book_id)

    # ==================== READING STATUS OPERATIONS ====================

    def get_book_status(self, book_id):
        """Get reading status for a book."""
        status = self.status_repo.find_by_book_id(book_id)
        if not status:
            raise ValueError(ErrorMessages.BOOK_NOT_FOUND)
        return status

    def update_status(self, book_id, new_status):
        """Update reading status with validation."""
        if not self.book_repo.exists(book_id):
            raise ValueError(ErrorMessages.BOOK_NOT_FOUND)

        if not BookStatus.is_valid(new_status):
            raise ValueError(ErrorMessages.INVALID_STATUS)

        return self.status_repo.update_status(book_id, new_status)

    def update_rating(self, book_id, rating):
        """Update book rating with validation."""
        if not self.book_repo.exists(book_id):
            raise ValueError(ErrorMessages.BOOK_NOT_FOUND)

        valid, msg = validate_rating_update({"rating": rating})
        if not valid:
            raise ValueError(msg)

        return self.status_repo.update_rating(book_id, rating)

    def update_progress(self, book_id, pages_read):
        """Update reading progress with validation."""
        if not self.book_repo.exists(book_id):
            raise ValueError(ErrorMessages.BOOK_NOT_FOUND)

        valid, msg = validate_progress_update({"pages_read": pages_read})
        if not valid:
            raise ValueError(msg)

        # Check pages_read doesn't exceed total pages
        progress = self.status_repo.get_reading_progress(book_id)
        if progress and progress.get("pages") and pages_read > progress["pages"]:
            raise ValueError(
                f"Pages read ({pages_read}) cannot exceed total pages ({progress['pages']})"
            )

        return self.status_repo.update_progress(book_id, pages_read)

    def update_notes(self, book_id, notes):
        """Update reading notes."""
        if not self.book_repo.exists(book_id):
            raise ValueError(ErrorMessages.BOOK_NOT_FOUND)
        return self.status_repo.update_notes(book_id, notes)

    def get_reading_progress(self, book_id):
        """Get reading progress percentage."""
        progress = self.status_repo.get_reading_progress(book_id)
        if not progress:
            raise ValueError(ErrorMessages.BOOK_NOT_FOUND)
        return progress

    # ==================== REVIEW OPERATIONS ====================

    def get_review(self, book_id):
        """Get review for a book."""
        if not self.book_repo.exists(book_id):
            raise ValueError(ErrorMessages.BOOK_NOT_FOUND)
        return self.review_repo.find_by_book_id(book_id)

    def create_or_update_review(self, book_id, rating, title, content, spoiler_warning=False):
        """Create or update review with validation."""
        if not self.book_repo.exists(book_id):
            raise ValueError(ErrorMessages.BOOK_NOT_FOUND)

        data = {
            "rating": rating,
            "title": title,
            "content": content,
            "spoiler_warning": spoiler_warning,
        }
        valid, msg = validate_review_data(data)
        if not valid:
            raise ValueError(f"Validation failed: {msg}")

        return self.review_repo.update(book_id, rating, title, content, spoiler_warning)

    def delete_review(self, book_id):
        """Delete review for a book."""
        if not self.book_repo.exists(book_id):
            raise ValueError(ErrorMessages.BOOK_NOT_FOUND)
        return self.review_repo.delete(book_id)

    # ==================== TBR LIST OPERATIONS ====================

    def get_tbr_list(self):
        """Get all TBR items ordered by priority."""
        return self.tbr_repo.find_all()

    def add_to_tbr(self, book_id, priority=0):
        """Add book to TBR list with validation."""
        if not self.book_repo.exists(book_id):
            raise ValueError(ErrorMessages.BOOK_NOT_FOUND)

        if self.tbr_repo.is_in_tbr(book_id):
            raise ValueError("Book is already in TBR list")

        return self.tbr_repo.add_book(book_id, priority)

    def remove_from_tbr(self, book_id):
        """Remove book from TBR list."""
        if not self.book_repo.exists(book_id):
            raise ValueError(ErrorMessages.BOOK_NOT_FOUND)
        return self.tbr_repo.remove_book(book_id)

    def reorder_tbr(self, items):
        """Reorder TBR list."""
        if not items:
            raise ValueError("items list cannot be empty")
        return self.tbr_repo.reorder_items(items)

    def get_next_to_read(self, limit=1):
        """Get next book(s) to read from TBR list."""
        return self.tbr_repo.get_next_to_read(limit)

    def get_tbr_count(self):
        """Get count of TBR items."""
        return self.tbr_repo.get_count()

    # ==================== STATISTICS OPERATIONS ====================

    def get_all_stats(self):
        """Get comprehensive reading statistics."""
        return self.stats_repo.get_all_stats()

    def get_reading_stats(self):
        """Get reading progress statistics."""
        return self.stats_repo.get_reading_progress_stats()

    def get_genre_stats(self):
        """Get books by genre statistics."""
        return self.stats_repo.get_books_by_genre()

    def get_rating_stats(self):
        """Get books by rating statistics."""
        return self.stats_repo.get_books_by_rating()

    def get_top_authors(self, limit=5):
        """Get top authors by book count."""
        return self.stats_repo.get_top_authors(limit)


# Global service instance
_service = None


def init_database_service():
    """Initialize the global database service."""
    global _service
    _service = DatabaseService()
    return _service


def get_database_service() -> DatabaseService:
    """Get the global database service."""
    global _service
    if _service is None:
        _service = init_database_service()
    return _service
