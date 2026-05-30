"""Repository for Book data access."""
from repositories.base_repository import BaseRepository


class BookRepository(BaseRepository):
    """Repository for managing books."""

    def find_by_id(self, book_id):
        """Find book by ID with author details."""
        query = """
            SELECT b.id, b.isbn, b.title, b.author_id, a.name as author_name,
                   b.publication_year, b.genre, b.description, b.cover_url, b.pages,
                   a.biography, a.country, a.website_url,
                   bs.status, bs.rating, bs.is_tbr, bs.pages_read, bs.notes,
                   bs.date_added, bs.date_started, bs.date_completed
            FROM books b
            JOIN authors a ON b.author_id = a.id
            LEFT JOIN book_status bs ON b.id = bs.book_id
            WHERE b.id = %s
        """
        return self.execute_query(query, [book_id], fetch_one=True)

    def find_all(self, limit=20, offset=0, status=None, genre=None, sort_by="title"):
        """Find all books with optional filtering and pagination."""
        query = """
            SELECT b.id, b.isbn, b.title, b.author_id, a.name as author_name,
                   b.publication_year, b.genre, b.description, b.cover_url, b.pages,
                   bs.status, bs.rating, bs.is_tbr, bs.pages_read, bs.date_completed
            FROM books b
            JOIN authors a ON b.author_id = a.id
            LEFT JOIN book_status bs ON b.id = bs.book_id
            WHERE 1=1
        """

        params = []

        if status:
            query += " AND bs.status = %s"
            params.append(status)

        if genre:
            query += " AND %s = ANY(b.genre)"
            params.append(genre)

        valid_sort_fields = ["title", "author_name", "publication_year", "date_completed"]
        sort_field = sort_by if sort_by in valid_sort_fields else "title"
        query += f" ORDER BY {sort_field} LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        return self.execute_query(query, params, fetch_all=True)

    def search(self, search_term, limit=50):
        """Search books by title, author, or genre."""
        query = """
            SELECT b.id, b.isbn, b.title, b.author_id, a.name as author_name,
                   b.publication_year, b.genre, b.description, b.cover_url, b.pages,
                   bs.status, bs.rating, bs.is_tbr
            FROM books b
            JOIN authors a ON b.author_id = a.id
            LEFT JOIN book_status bs ON b.id = bs.book_id
            WHERE LOWER(b.title) LIKE LOWER(%s)
               OR LOWER(a.name) LIKE LOWER(%s)
               OR EXISTS (SELECT 1 FROM UNNEST(b.genre) as g WHERE LOWER(g) LIKE LOWER(%s))
            LIMIT %s
        """

        search_param = f"%{search_term}%"
        return self.execute_query(query, [search_param, search_param, search_param, limit], fetch_all=True)

    def create(self, title, author_id, isbn=None, publication_year=None, genre=None, description=None, cover_url=None, pages=None):
        """Create a new book."""
        query = """
            INSERT INTO books (isbn, title, author_id, publication_year, genre, description, cover_url, pages)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """

        params = [isbn, title, author_id, publication_year, genre, description, cover_url, pages]
        book_id = self.execute_insert(query, params)

        # Initialize book_status
        status_query = """
            INSERT INTO book_status (book_id, status, date_added)
            VALUES (%s, 'unread', CURRENT_TIMESTAMP)
        """
        self.execute_update(status_query, [book_id])

        return book_id

    def update(self, book_id, **kwargs):
        """Update book fields dynamically."""
        update_fields = []
        params = []

        allowed_fields = ["title", "author_id", "publication_year", "genre", "description", "cover_url", "pages"]

        for field in allowed_fields:
            if field in kwargs:
                update_fields.append(f"{field} = %s")
                params.append(kwargs[field])

        if not update_fields:
            return False

        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        params.append(book_id)

        query = f"UPDATE books SET {', '.join(update_fields)} WHERE id = %s"
        return self.execute_update(query, params) > 0

    def delete(self, book_id):
        """Delete a book (cascade will handle related records)."""
        query = "DELETE FROM books WHERE id = %s"
        return self.execute_update(query, [book_id]) > 0

    def exists(self, book_id):
        """Check if book exists."""
        query = "SELECT id FROM books WHERE id = %s"
        return self.execute_query(query, [book_id], fetch_one=True) is not None
