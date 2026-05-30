"""Repository for TBR (To-Be-Read) list data access."""
from repositories.base_repository import BaseRepository


class TBRRepository(BaseRepository):
    """Repository for managing TBR lists."""

    def find_by_id(self, item_id):
        """Find TBR item by ID."""
        query = """
            SELECT ti.id, ti.book_id, ti.priority,
                   b.title, b.author_id, a.name as author_name,
                   b.pages, b.genre, b.cover_url
            FROM tbr_items ti
            JOIN books b ON ti.book_id = b.id
            JOIN authors a ON b.author_id = a.id
            WHERE ti.id = %s
        """
        return self.execute_query(query, [item_id], fetch_one=True)

    def find_all(self):
        """Get all TBR items ordered by priority."""
        query = """
            SELECT ti.id, ti.book_id, ti.priority,
                   b.title, b.author_id, a.name as author_name,
                   b.pages, b.genre, b.cover_url,
                   bs.status, bs.date_added
            FROM tbr_items ti
            JOIN books b ON ti.book_id = b.id
            JOIN authors a ON b.author_id = a.id
            LEFT JOIN book_status bs ON b.id = bs.book_id
            ORDER BY ti.priority ASC, b.title ASC
        """
        return self.execute_query(query, fetch_all=True)

    def get_default_list(self):
        """Get or create the default TBR list."""
        query = "SELECT id FROM tbr_list LIMIT 1"
        result = self.execute_query(query, fetch_one=True)

        if result:
            return result["id"]
        else:
            # Create default list
            create_query = """
                INSERT INTO tbr_list (name, description)
                VALUES ('My Reading List', 'Books I want to read')
                RETURNING id
            """
            return self.execute_insert(create_query, [])

    def add_book(self, book_id, priority=0):
        """Add a book to TBR list."""
        tbr_list_id = self.get_default_list()

        query = """
            INSERT INTO tbr_items (tbr_list_id, book_id, priority)
            VALUES (%s, %s, %s)
            RETURNING id
        """

        item_id = self.execute_insert(query, [tbr_list_id, book_id, priority])

        # Update book_status
        status_query = "UPDATE book_status SET is_tbr = TRUE WHERE book_id = %s"
        self.execute_update(status_query, [book_id])

        return item_id

    def remove_book(self, book_id):
        """Remove a book from TBR list."""
        query = "DELETE FROM tbr_items WHERE book_id = %s"
        result = self.execute_update(query, [book_id]) > 0

        # Update book_status
        if result:
            status_query = "UPDATE book_status SET is_tbr = FALSE WHERE book_id = %s"
            self.execute_update(status_query, [book_id])

        return result

    def update_priority(self, item_id, priority):
        """Update priority for a TBR item."""
        query = "UPDATE tbr_items SET priority = %s WHERE id = %s"
        return self.execute_update(query, [priority, item_id]) > 0

    def reorder_items(self, items):
        """Reorder multiple TBR items."""
        for item in items:
            self.update_priority(item["id"], item["priority"])
        return True

    def get_count(self):
        """Get total count of TBR items."""
        query = "SELECT COUNT(*) as count FROM tbr_items"
        result = self.execute_query(query, fetch_one=True)
        return result["count"] if result else 0

    def is_in_tbr(self, book_id):
        """Check if book is in TBR list."""
        query = "SELECT id FROM tbr_items WHERE book_id = %s"
        return self.execute_query(query, [book_id], fetch_one=True) is not None

    def get_next_to_read(self, limit=1):
        """Get next book(s) to read (highest priority)."""
        query = """
            SELECT ti.id, ti.book_id, ti.priority,
                   b.title, b.author_id, a.name as author_name,
                   b.pages, b.genre, b.description
            FROM tbr_items ti
            JOIN books b ON ti.book_id = b.id
            JOIN authors a ON b.author_id = a.id
            ORDER BY ti.priority ASC
            LIMIT %s
        """
        return self.execute_query(query, [limit], fetch_all=True)
