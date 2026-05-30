"""Book status management endpoints."""
from flask import request, jsonify, current_app
from routes import book_status_bp


def get_service():
    """Get database service from app container (DI)."""
    return current_app.container.database


@book_status_bp.route("/<int:book_id>/status", methods=["GET"])
def get_book_status(book_id):
    """Get reading status for a book."""
    try:
        service = get_service()
        status = service.get_book_status(book_id)
        return jsonify({"status": "success", "data": status})

    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@book_status_bp.route("/<int:book_id>/status", methods=["PUT"])
def update_book_status(book_id):
    """Update reading status for a book."""
    try:
        data = request.get_json() or {}
        service = get_service()
        service.update_status(book_id, data.get("status"))

        return jsonify({"status": "success", "message": "Status updated successfully"})

    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@book_status_bp.route("/<int:book_id>/rating", methods=["PUT"])
def update_book_rating(book_id):
    """Update rating for a book."""
    try:
        data = request.get_json() or {}
        service = get_service()
        service.update_rating(book_id, data.get("rating"))

        return jsonify({"status": "success", "message": "Rating updated successfully"})

    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@book_status_bp.route("/<int:book_id>/progress", methods=["PUT"])
def update_reading_progress(book_id):
    """Update reading progress for a book."""
    try:
        data = request.get_json() or {}
        service = get_service()
        service.update_progress(book_id, data.get("pages_read"))

        return jsonify({"status": "success", "message": "Progress updated successfully"})

    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@book_status_bp.route("/<int:book_id>/notes", methods=["PUT"])
def update_book_notes(book_id):
    """Update notes for a book."""
    try:
        data = request.get_json() or {}
        service = get_service()
        service.update_notes(book_id, data.get("notes"))

        return jsonify({"status": "success", "message": "Notes updated successfully"})

    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
