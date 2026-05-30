"""Repository for BookStatus data access."""
from repositories.base_repository import BaseRepository


class BookStatusRepository(BaseRepository):
    """Repository for managing book reading status."""

    def find_by_book_id(self, book_id):
        """Get reading status for a book."""
        query = """
            SELECT bs.status, bs.rating, bs.is_tbr, bs.pages_read, bs.notes,
                   bs.date_added, bs.date_started, bs.date_completed,
                   b.title, b.pages
            FROM book_status bs
            JOIN books b ON bs.book_id = b.id
            WHERE bs.book_id = %s
        """
        return self.execute_query(query, [book_id], fetch_one=True)

    def find_by_id(self, book_id):
        """Alias for find_by_book_id for base class compatibility."""
        return self.find_by_book_id(book_id)

    def find_all(self):
        """Get all book statuses."""
        query = "SELECT * FROM book_status"
        return self.execute_query(query, fetch_all=True)

    def update_status(self, book_id, status):
        """Update reading status."""
        query = """
            UPDATE book_status
            SET status = %s,
                date_started = CASE WHEN %s = 'reading' THEN COALESCE(date_started, CURRENT_TIMESTAMP) ELSE date_started END,
                date_completed = CASE WHEN %s = 'completed' THEN COALESCE(date_completed, CURRENT_TIMESTAMP) ELSE date_completed END,
                updated_at = CURRENT_TIMESTAMP
            WHERE book_id = %s
        """
        return self.execute_update(query, [status, status, status, book_id]) > 0

    def update_rating(self, book_id, rating):
        """Update book rating."""
        query = """
            UPDATE book_status
            SET rating = %s, updated_at = CURRENT_TIMESTAMP
            WHERE book_id = %s
        """
        return self.execute_update(query, [rating, book_id]) > 0

    def update_progress(self, book_id, pages_read):
        """Update reading progress."""
        query = """
            UPDATE book_status
            SET pages_read = %s, updated_at = CURRENT_TIMESTAMP
            WHERE book_id = %s
        """
        return self.execute_update(query, [pages_read, book_id]) > 0

    def update_notes(self, book_id, notes):
        """Update reading notes."""
        query = """
            UPDATE book_status
            SET notes = %s, updated_at = CURRENT_TIMESTAMP
            WHERE book_id = %s
        """
        return self.execute_update(query, [notes, book_id]) > 0

    def get_reading_progress(self, book_id):
        """Get reading progress for a book."""
        query = """
            SELECT bs.pages_read, b.pages,
                   ROUND((bs.pages_read::float / NULLIF(b.pages, 0) * 100)::numeric, 2) as progress_percent
            FROM book_status bs
            JOIN books b ON bs.book_id = b.id
            WHERE bs.book_id = %s
        """
        return self.execute_query(query, [book_id], fetch_one=True)

    def get_by_status(self, status, limit=50):
        """Get books by reading status."""
        query = """
            SELECT b.id, b.title, a.name as author_name, bs.pages_read, b.pages
            FROM book_status bs
            JOIN books b ON bs.book_id = b.id
            JOIN authors a ON b.author_id = a.id
            WHERE bs.status = %s
            LIMIT %s
        """
        return self.execute_query(query, [status, limit], fetch_all=True)
