"""Book status management endpoints."""
from flask import request, jsonify
from routes import book_status_bp
from db import get_db
from utils.validators import validate_status_update, validate_rating_update, validate_progress_update
from utils.constants import ErrorMessages


@book_status_bp.route("/<int:book_id>/status", methods=["GET"])
def get_book_status(book_id):
    """Get reading status for a book."""
    try:
        db = get_db()

        query = """
            SELECT bs.status, bs.rating, bs.is_tbr, bs.pages_read, bs.notes,
                   bs.date_added, bs.date_started, bs.date_completed,
                   b.title, b.pages
            FROM book_status bs
            JOIN books b ON bs.book_id = b.id
            WHERE bs.book_id = %s
        """

        status = db.execute_query(query, [book_id], fetch_one=True)

        if not status:
            return jsonify({"status": "error", "message": ErrorMessages.BOOK_NOT_FOUND}), 404

        return jsonify({"status": "success", "data": status})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@book_status_bp.route("/<int:book_id>/status", methods=["PUT"])
def update_book_status(book_id):
    """Update reading status for a book."""
    try:
        data = request.get_json() or {}

        # Validate
        valid, msg = validate_status_update(data)
        if not valid:
            return jsonify({"status": "error", "message": msg}), 400

        db = get_db()

        # Check if book exists
        check_query = "SELECT id FROM book_status WHERE book_id = %s"
        if not db.execute_query(check_query, [book_id], fetch_one=True):
            return jsonify({"status": "error", "message": ErrorMessages.BOOK_NOT_FOUND}), 404

        # Update status
        query = """
            UPDATE book_status
            SET status = %s,
                date_started = CASE WHEN %s = 'reading' THEN COALESCE(date_started, CURRENT_TIMESTAMP) ELSE date_started END,
                date_completed = CASE WHEN %s = 'completed' THEN COALESCE(date_completed, CURRENT_TIMESTAMP) ELSE date_completed END,
                updated_at = CURRENT_TIMESTAMP
            WHERE book_id = %s
        """

        status = data["status"]
        db.execute_update(query, [status, status, status, book_id])

        return jsonify({"status": "success", "message": "Status updated successfully"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@book_status_bp.route("/<int:book_id>/rating", methods=["PUT"])
def update_book_rating(book_id):
    """Update rating for a book."""
    try:
        data = request.get_json() or {}

        # Validate
        valid, msg = validate_rating_update(data)
        if not valid:
            return jsonify({"status": "error", "message": msg}), 400

        db = get_db()

        # Check if book exists
        check_query = "SELECT id FROM book_status WHERE book_id = %s"
        if not db.execute_query(check_query, [book_id], fetch_one=True):
            return jsonify({"status": "error", "message": ErrorMessages.BOOK_NOT_FOUND}), 404

        query = """
            UPDATE book_status
            SET rating = %s, updated_at = CURRENT_TIMESTAMP
            WHERE book_id = %s
        """

        db.execute_update(query, [data["rating"], book_id])

        return jsonify({"status": "success", "message": "Rating updated successfully"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@book_status_bp.route("/<int:book_id>/progress", methods=["PUT"])
def update_reading_progress(book_id):
    """Update reading progress for a book."""
    try:
        data = request.get_json() or {}

        # Validate
        valid, msg = validate_progress_update(data)
        if not valid:
            return jsonify({"status": "error", "message": msg}), 400

        db = get_db()

        # Check if book exists and get total pages
        check_query = "SELECT bs.id, b.pages FROM book_status bs JOIN books b ON bs.book_id = b.id WHERE bs.book_id = %s"
        result = db.execute_query(check_query, [book_id], fetch_one=True)

        if not result:
            return jsonify({"status": "error", "message": ErrorMessages.BOOK_NOT_FOUND}), 404

        pages_read = data["pages_read"]
        total_pages = result.get("pages")

        # Validate pages_read is not more than total pages
        if total_pages and pages_read > total_pages:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": f"Pages read ({pages_read}) cannot exceed total pages ({total_pages})",
                    }
                ),
                400,
            )

        query = """
            UPDATE book_status
            SET pages_read = %s, updated_at = CURRENT_TIMESTAMP
            WHERE book_id = %s
        """

        db.execute_update(query, [pages_read, book_id])

        return jsonify({"status": "success", "message": "Progress updated successfully"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@book_status_bp.route("/<int:book_id>/notes", methods=["PUT"])
def update_book_notes(book_id):
    """Update notes for a book."""
    try:
        data = request.get_json() or {}

        if "notes" not in data:
            return jsonify({"status": "error", "message": "notes field is required"}), 400

        db = get_db()

        # Check if book exists
        check_query = "SELECT id FROM book_status WHERE book_id = %s"
        if not db.execute_query(check_query, [book_id], fetch_one=True):
            return jsonify({"status": "error", "message": ErrorMessages.BOOK_NOT_FOUND}), 404

        query = """
            UPDATE book_status
            SET notes = %s, updated_at = CURRENT_TIMESTAMP
            WHERE book_id = %s
        """

        db.execute_update(query, [data["notes"], book_id])

        return jsonify({"status": "success", "message": "Notes updated successfully"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
