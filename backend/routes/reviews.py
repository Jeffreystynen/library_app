"""Book review endpoints."""
from flask import request, jsonify, current_app
from routes import reviews_bp


def get_service():
    """Get database service from app container (DI)."""
    return current_app.container.database


@reviews_bp.route("/<int:book_id>/reviews", methods=["GET"])
def get_reviews(book_id):
    """Get reviews for a book."""
    try:
        service = get_service()
        reviews = service.get_review(book_id)
        return jsonify({"status": "success", "data": reviews or []})

    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@reviews_bp.route("/<int:book_id>/reviews", methods=["POST"])
def create_or_update_review(book_id):
    """Create or update review for a book."""
    try:
        data = request.get_json() or {}
        service = get_service()
        review_id = service.create_or_update_review(
            book_id=book_id,
            rating=data.get("rating"),
            title=data.get("title"),
            content=data.get("content"),
            spoiler_warning=data.get("spoiler_warning", False),
        )

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Review created or updated successfully",
                    "id": review_id,
                }
            ),
            201,
        )

    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@reviews_bp.route("/<int:book_id>/reviews", methods=["DELETE"])
def delete_review(book_id):
    """Delete review for a book."""
    try:
        service = get_service()
        service.delete_review(book_id)

        return jsonify({"status": "success", "message": "Review deleted successfully"})

    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
