"""Repository for Statistics and Analytics data access."""
from services.base_repository import BaseRepository


class StatsRepository(BaseRepository):
    """Repository for reading statistics and analytics."""

    def find_by_id(self, id):
        """Not applicable for stats - override with pass."""
        pass

    def find_all(self):
        """Not applicable for stats - override with pass."""
        pass

    def get_total_books(self):
        """Get total count of books in library."""
        query = "SELECT COUNT(*) as count FROM books"
        result = self.execute_query(query, fetch_one=True)
        return result["count"] if result else 0

    def get_books_by_status(self):
        """Get count of books by reading status."""
        query = """
            SELECT bs.status, COUNT(*) as count
            FROM book_status bs
            GROUP BY bs.status
            ORDER BY bs.status
        """
        return self.execute_query(query, fetch_all=True)

    def get_books_by_genre(self):
        """Get count of books by genre."""
        query = """
            SELECT genre, COUNT(*) as count
            FROM books b, LATERAL UNNEST(b.genre) as genre
            GROUP BY genre
            ORDER BY count DESC
        """
        return self.execute_query(query, fetch_all=True)

    def get_books_by_rating(self):
        """Get count of books by rating."""
        query = """
            SELECT bs.rating, COUNT(*) as count
            FROM book_status bs
            WHERE bs.rating IS NOT NULL
            GROUP BY bs.rating
            ORDER BY bs.rating DESC
        """
        return self.execute_query(query, fetch_all=True)

    def get_average_rating(self):
        """Get average rating of all reviewed books."""
        query = """
            SELECT ROUND(AVG(bs.rating)::numeric, 2) as average_rating,
                   COUNT(*) as reviewed_books
            FROM book_status bs
            WHERE bs.rating IS NOT NULL
        """
        return self.execute_query(query, fetch_one=True)

    def get_pages_statistics(self):
        """Get statistics about pages read."""
        query = """
            SELECT COUNT(*) as total_books_read,
                   COALESCE(SUM(bs.pages_read), 0) as total_pages_started,
                   ROUND(AVG(b.pages)::numeric, 1) as average_book_length
            FROM book_status bs
            JOIN books b ON bs.book_id = b.id
            WHERE bs.status IN ('reading', 'completed')
        """
        return self.execute_query(query, fetch_one=True)

    def get_top_authors(self, limit=5):
        """Get top authors by number of books."""
        query = """
            SELECT a.name, COUNT(*) as count
            FROM books b
            JOIN authors a ON b.author_id = a.id
            GROUP BY a.id, a.name
            ORDER BY count DESC
            LIMIT %s
        """
        return self.execute_query(query, [limit], fetch_all=True)

    def get_reading_progress_stats(self):
        """Get overall reading progress statistics."""
        query = """
            SELECT
                COUNT(CASE WHEN bs.status = 'completed' THEN 1 END) as completed_books,
                COUNT(CASE WHEN bs.status = 'reading' THEN 1 END) as books_reading,
                COUNT(CASE WHEN bs.status = 'unread' THEN 1 END) as unread_books,
                COUNT(CASE WHEN bs.is_tbr = TRUE THEN 1 END) as tbr_count,
                COUNT(CASE WHEN bs.rating IS NOT NULL THEN 1 END) as rated_books
            FROM book_status bs
        """
        return self.execute_query(query, fetch_one=True)

    def get_all_stats(self):
        """Get comprehensive reading statistics."""
        return {
            "total_books": self.get_total_books(),
            "by_status": self.get_books_by_status(),
            "by_genre": self.get_books_by_genre(),
            "by_rating": self.get_books_by_rating(),
            "average_rating": self.get_average_rating(),
            "pages_statistics": self.get_pages_statistics(),
            "top_authors": self.get_top_authors(),
            "progress": self.get_reading_progress_stats(),
        }
