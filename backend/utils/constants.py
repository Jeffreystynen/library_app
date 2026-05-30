"""Application constants."""

# Book Status enums
class BookStatus:
    """Valid book statuses."""

    UNREAD = "unread"
    READING = "reading"
    COMPLETED = "completed"
    DNF = "dnf"  # Did Not Finish

    @classmethod
    def all(cls):
        """Return all valid statuses."""
        return [cls.UNREAD, cls.READING, cls.COMPLETED, cls.DNF]

    @classmethod
    def is_valid(cls, status):
        """Check if status is valid."""
        return status in cls.all()


# Rating constants
class Rating:
    """Valid rating range."""

    MIN = 1
    MAX = 5

    @classmethod
    def is_valid(cls, rating):
        """Check if rating is valid."""
        if rating is None:
            return True  # Ratings are optional
        try:
            r = int(rating)
            return cls.MIN <= r <= cls.MAX
        except (ValueError, TypeError):
            return False


# Pagination
class Pagination:
    """Pagination constants."""

    DEFAULT_LIMIT = 20
    MAX_LIMIT = 100
    DEFAULT_OFFSET = 0

    @classmethod
    def validate_limit(cls, limit):
        """Validate and normalize limit."""
        try:
            limit = int(limit) if limit else cls.DEFAULT_LIMIT
            return min(limit, cls.MAX_LIMIT)
        except (ValueError, TypeError):
            return cls.DEFAULT_LIMIT

    @classmethod
    def validate_offset(cls, offset):
        """Validate and normalize offset."""
        try:
            offset = int(offset) if offset else cls.DEFAULT_OFFSET
            return max(offset, 0)
        except (ValueError, TypeError):
            return cls.DEFAULT_OFFSET


# Error messages
class ErrorMessages:
    """Standard error messages."""

    INVALID_STATUS = "Invalid book status. Must be one of: unread, reading, completed, dnf"
    INVALID_RATING = f"Invalid rating. Must be between {Rating.MIN} and {Rating.MAX}"
    BOOK_NOT_FOUND = "Book not found"
    INVALID_REQUEST = "Invalid request data"
    DATABASE_ERROR = "Database error occurred"
    MISSING_FIELD = "Missing required field: {}"
    INVALID_FIELD = "Invalid value for field: {}"
