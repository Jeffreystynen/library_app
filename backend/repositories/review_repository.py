"""Repository for Review data access."""
from repositories.base_repository import BaseRepository


class ReviewRepository(BaseRepository):
    """Repository for managing book reviews."""

    def find_by_book_id(self, book_id):
        """Get review for a book."""
        query = """
            SELECT id, rating, title, content, spoiler_warning, created_at, updated_at
            FROM reviews
            WHERE book_id = %s
        """
        return self.execute_query(query, [book_id], fetch_one=True)

    def find_by_id(self, review_id):
        """Find review by ID."""
        query = """
            SELECT id, book_id, rating, title, content, spoiler_warning, created_at, updated_at
            FROM reviews
            WHERE id = %s
        """
        return self.execute_query(query, [review_id], fetch_one=True)

    def find_all(self, limit=50, offset=0):
        """Get all reviews with pagination."""
        query = """
            SELECT r.id, r.book_id, b.title as book_title, r.rating, r.title,
                   r.content, r.spoiler_warning, r.created_at, r.updated_at
            FROM reviews r
            JOIN books b ON r.book_id = b.id
            ORDER BY r.created_at DESC
            LIMIT %s OFFSET %s
        """
        return self.execute_query(query, [limit, offset], fetch_all=True)

    def create(self, book_id, rating, title, content, spoiler_warning=False):
        """Create a new review."""
        query = """
            INSERT INTO reviews (book_id, rating, title, content, spoiler_warning, created_at)
            VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            RETURNING id
        """
        return self.execute_insert(query, [book_id, rating, title, content, spoiler_warning])

    def update(self, book_id, rating, title, content, spoiler_warning=False):
        """Create or update review for a book."""
        # Check if review exists
        check_query = "SELECT id FROM reviews WHERE book_id = %s"
        existing = self.execute_query(check_query, [book_id], fetch_one=True)

        if existing:
            # Update
            query = """
                UPDATE reviews
                SET rating = %s,
                    title = %s,
                    content = %s,
                    spoiler_warning = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE book_id = %s
            """
            self.execute_update(query, [rating, title, content, spoiler_warning, book_id])
            return existing["id"]
        else:
            # Create
            return self.create(book_id, rating, title, content, spoiler_warning)

    def delete(self, book_id):
        """Delete review for a book."""
        query = "DELETE FROM reviews WHERE book_id = %s"
        return self.execute_update(query, [book_id]) > 0

    def get_by_rating(self, min_rating=None, limit=50):
        """Get reviews by minimum rating."""
        if min_rating is None:
            query = """
                SELECT r.id, b.title as book_title, r.rating, r.title,
                       r.content, r.created_at
                FROM reviews r
                JOIN books b ON r.book_id = b.id
                ORDER BY r.rating DESC, r.created_at DESC
                LIMIT %s
            """
            return self.execute_query(query, [limit], fetch_all=True)
        else:
            query = """
                SELECT r.id, b.title as book_title, r.rating, r.title,
                       r.content, r.created_at
                FROM reviews r
                JOIN books b ON r.book_id = b.id
                WHERE r.rating >= %s
                ORDER BY r.rating DESC, r.created_at DESC
                LIMIT %s
            """
            return self.execute_query(query, [min_rating, limit], fetch_all=True)

    def get_average_rating(self, book_id):
        """Get average rating for a book."""
        query = """
            SELECT ROUND(AVG(rating)::numeric, 2) as average_rating,
                   COUNT(*) as review_count
            FROM reviews
            WHERE book_id = %s
        """
        return self.execute_query(query, [book_id], fetch_one=True)

    def exists(self, book_id):
        """Check if review exists for a book."""
        query = "SELECT id FROM reviews WHERE book_id = %s"
        return self.execute_query(query, [book_id], fetch_one=True) is not None
