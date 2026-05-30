"""Book management endpoints."""
from flask import request, jsonify
from routes import books_bp
from db import get_db
from utils.validators import validate_book_data, validate_required_fields
from utils.constants import Pagination, ErrorMessages


@books_bp.route("", methods=["GET"])
def list_books():
    """Get all books with optional filtering and pagination."""
    # Get query parameters
    limit = request.args.get("limit", Pagination.DEFAULT_LIMIT)
    offset = request.args.get("offset", Pagination.DEFAULT_OFFSET)
    status = request.args.get("status")
    genre = request.args.get("genre")
    sort_by = request.args.get("sort_by", "title")

    # Validate pagination
    limit = Pagination.validate_limit(limit)
    offset = Pagination.validate_offset(offset)

    try:
        db = get_db()

        # Build query
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

        # Add filters
        if status:
            query += " AND bs.status = %s"
            params.append(status)

        if genre:
            query += " AND %s = ANY(b.genre)"
            params.append(genre)

        # Add sorting
        valid_sort_fields = ["title", "author_name", "publication_year", "date_completed"]
        sort_field = sort_by if sort_by in valid_sort_fields else "title"
        query += f" ORDER BY {sort_field}"

        # Add pagination
        query += " LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        books = db.execute_query(query, params, fetch_all=True)

        return jsonify(
            {
                "status": "success",
                "count": len(books),
                "limit": limit,
                "offset": offset,
                "data": books,
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@books_bp.route("/<int:book_id>", methods=["GET"])
def get_book(book_id):
    """Get a specific book by ID."""
    try:
        db = get_db()

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

        book = db.execute_query(query, [book_id], fetch_one=True)

        if not book:
            return jsonify({"status": "error", "message": ErrorMessages.BOOK_NOT_FOUND}), 404

        return jsonify({"status": "success", "data": book})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@books_bp.route("", methods=["POST"])
def create_book():
    """Create a new book."""
    try:
        data = request.get_json() or {}

        # Validate required fields
        valid, msg = validate_required_fields(data, ["title", "author_id"])
        if not valid:
            return jsonify({"status": "error", "message": msg}), 400

        # Validate data
        errors = validate_book_data(data)
        if errors is not True:
            return jsonify({"status": "error", "message": "Validation failed", "errors": errors}), 400

        db = get_db()

        query = """
            INSERT INTO books (isbn, title, author_id, publication_year, genre, description, cover_url, pages)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """

        params = [
            data.get("isbn"),
            data["title"],
            data["author_id"],
            data.get("publication_year"),
            data.get("genre"),
            data.get("description"),
            data.get("cover_url"),
            data.get("pages"),
        ]

        book_id = db.execute_insert(query, params)

        # Initialize book status
        status_query = """
            INSERT INTO book_status (book_id, status, date_added)
            VALUES (%s, 'unread', CURRENT_TIMESTAMP)
        """
        db.execute_update(status_query, [book_id])

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Book created successfully",
                    "id": book_id,
                }
            ),
            201,
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@books_bp.route("/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    """Update book information."""
    try:
        data = request.get_json() or {}

        # Validate data
        errors = validate_book_data(data)
        if errors is not True:
            return jsonify({"status": "error", "message": "Validation failed", "errors": errors}), 400

        db = get_db()

        # Check if book exists
        check_query = "SELECT id FROM books WHERE id = %s"
        if not db.execute_query(check_query, [book_id], fetch_one=True):
            return jsonify({"status": "error", "message": ErrorMessages.BOOK_NOT_FOUND}), 404

        # Build update query dynamically
        update_fields = []
        params = []

        for field in ["title", "author_id", "publication_year", "genre", "description", "cover_url", "pages"]:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])

        if not update_fields:
            return jsonify({"status": "error", "message": "No fields to update"}), 400

        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        params.append(book_id)

        query = f"UPDATE books SET {', '.join(update_fields)} WHERE id = %s"
        db.execute_update(query, params)

        return jsonify({"status": "success", "message": "Book updated successfully"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@books_bp.route("/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    """Delete a book."""
    try:
        db = get_db()

        # Check if book exists
        check_query = "SELECT id FROM books WHERE id = %s"
        if not db.execute_query(check_query, [book_id], fetch_one=True):
            return jsonify({"status": "error", "message": ErrorMessages.BOOK_NOT_FOUND}), 404

        # Delete book (cascade will handle book_status, reviews, etc.)
        query = "DELETE FROM books WHERE id = %s"
        db.execute_update(query, [book_id])

        return jsonify({"status": "success", "message": "Book deleted successfully"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@books_bp.route("/search", methods=["GET"])
def search_books():
    """Search books by title, author, or genre."""
    try:
        query_str = request.args.get("q", "").strip()

        if not query_str or len(query_str) < 2:
            return jsonify({"status": "error", "message": "Search query must be at least 2 characters"}), 400

        db = get_db()

        query = """
            SELECT b.id, b.isbn, b.title, b.author_id, a.name as author_name,
                   b.publication_year, b.genre, b.description, b.cover_url, b.pages,
                   bs.status, bs.rating, bs.is_tbr
            FROM books b
            JOIN authors a ON b.author_id = a.id
            LEFT JOIN book_status bs ON b.id = bs.book_id
            WHERE LOWER(b.title) LIKE LOWER(%s)
               OR LOWER(a.name) LIKE LOWER(%s)
               OR LOWER(ANY(b.genre)) LIKE LOWER(%s)
            LIMIT 50
        """

        search_term = f"%{query_str}%"
        books = db.execute_query(query, [search_term, search_term, search_term], fetch_all=True)

        return jsonify({"status": "success", "count": len(books), "data": books})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
