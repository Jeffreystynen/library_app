"""Book management endpoints."""
from flask import request, jsonify, current_app
from routes import books_bp
from utils.constants import Pagination, ErrorMessages


def get_service():
    """Get database service from app container (DI)."""
    return current_app.container.database


@books_bp.route("", methods=["GET"])
def list_books():
    """Get all books with optional filtering and pagination."""
    try:
        # Get query parameters
        limit = request.args.get("limit", Pagination.DEFAULT_LIMIT)
        offset = request.args.get("offset", Pagination.DEFAULT_OFFSET)
        status = request.args.get("status")
        genre = request.args.get("genre")
        sort_by = request.args.get("sort_by", "title")

        # Validate pagination
        limit = Pagination.validate_limit(limit)
        offset = Pagination.validate_offset(offset)

        # Get service and call it
        service = get_service()
        books = service.list_books(limit, offset, status, genre, sort_by)

        return jsonify(
            {
                "status": "success",
                "count": len(books) if books else 0,
                "limit": limit,
                "offset": offset,
                "data": books or [],
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@books_bp.route("/<int:book_id>", methods=["GET"])
def get_book(book_id):
    """Get a specific book by ID."""
    try:
        service = get_service()
        book = service.get_book(book_id)
        return jsonify({"status": "success", "data": book})

    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@books_bp.route("", methods=["POST"])
def create_book():
    """Create a new book."""
    try:
        data = request.get_json() or {}

        service = get_service()
        book_id = service.create_book(
            title=data.get("title"),
            author_id=data.get("author_id"),
            isbn=data.get("isbn"),
            publication_year=data.get("publication_year"),
            genre=data.get("genre"),
            description=data.get("description"),
            cover_url=data.get("cover_url"),
            pages=data.get("pages"),
        )

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

    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@books_bp.route("/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    """Update book information."""
    try:
        data = request.get_json() or {}

        service = get_service()
        service.update_book(book_id, **data)

        return jsonify({"status": "success", "message": "Book updated successfully"})

    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@books_bp.route("/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    """Delete a book."""
    try:
        service = get_service()
        service.delete_book(book_id)

        return jsonify({"status": "success", "message": "Book deleted successfully"})

    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@books_bp.route("/search", methods=["GET"])
def search_books():
    """Search books by title, author, or genre."""
    try:
        query_str = request.args.get("q", "").strip()

        if not query_str or len(query_str) < 2:
            return jsonify({"status": "error", "message": "Search query must be at least 2 characters"}), 400

        service = get_service()
        books = service.search_books(query_str)

        return jsonify({"status": "success", "count": len(books) if books else 0, "data": books or []})

    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@books_bp.route("/<int:book_id>/prediction", methods=["GET"])
def predict_completion(book_id):
    """Predict reading completion date using linear regression on reading history."""
    try:
        service = get_service()
        prediction = service.predict_completion(book_id)

        return jsonify({"status": "success", "data": prediction})

    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
