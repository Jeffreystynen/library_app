"""Repository for Reading Sessions data access."""
from repositories.base_repository import BaseRepository


class ReadingSessionRepository(BaseRepository):
    """Repository for managing reading sessions."""

    def find_by_id(self, session_id):
        """Find reading session by ID."""
        query = """
            SELECT id, book_id, session_date, pages_read, duration_minutes, notes, created_at
            FROM reading_sessions
            WHERE id = %s
        """
        return self.execute_query(query, [session_id], fetch_one=True)

    def find_all(self):
        """Get all reading sessions ordered by date."""
        query = """
            SELECT id, book_id, session_date, pages_read, duration_minutes, notes, created_at
            FROM reading_sessions
            ORDER BY session_date ASC
        """
        return self.execute_query(query, fetch_all=True)

    def get_daily_pages(self, book_id=None):
        """Get aggregated daily page totals, optionally filtered by book.

        Returns list of dicts with 'session_date' and 'pages_read' keys,
        sorted by date ascending.

        Args:
            book_id: if provided, aggregate only sessions for this book;
                    if None, aggregate across all books (global reading pace)
        """
        if book_id:
            query = """
                SELECT session_date, SUM(pages_read) as pages_read
                FROM reading_sessions
                WHERE book_id = %s
                GROUP BY session_date
                ORDER BY session_date ASC
            """
            return self.execute_query(query, [book_id], fetch_all=True)
        else:
            query = """
                SELECT session_date, SUM(pages_read) as pages_read
                FROM reading_sessions
                GROUP BY session_date
                ORDER BY session_date ASC
            """
            return self.execute_query(query, fetch_all=True)

    def get_sessions_for_book(self, book_id):
        """Get all reading sessions for a specific book."""
        query = """
            SELECT id, book_id, session_date, pages_read, duration_minutes, notes, created_at
            FROM reading_sessions
            WHERE book_id = %s
            ORDER BY session_date ASC
        """
        return self.execute_query(query, [book_id], fetch_all=True)

    def create(self, book_id, session_date, pages_read, duration_minutes=None, notes=None):
        """Create a new reading session."""
        query = """
            INSERT INTO reading_sessions (book_id, session_date, pages_read, duration_minutes, notes)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """
        params = [book_id, session_date, pages_read, duration_minutes, notes]
        return self.execute_insert(query, params)

    def delete(self, session_id):
        """Delete a reading session."""
        query = "DELETE FROM reading_sessions WHERE id = %s"
        return self.execute_update(query, [session_id]) > 0
