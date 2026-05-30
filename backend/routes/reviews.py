"""Book review endpoints."""
from flask import request, jsonify
from routes import reviews_bp
from db import get_db
from utils.validators import validate_review_data
from utils.constants import ErrorMessages


@reviews_bp.route("/<int:book_id>/reviews", methods=["GET"])
def get_reviews(book_id):
    """Get reviews for a book."""
    try:
        db = get_db()

        # Check book exists
        check_query = "SELECT id FROM books WHERE id = %s"
        if not db.execute_query(check_query, [book_id], fetch_one=True):
            return jsonify({"status": "error", "message": ErrorMessages.BOOK_NOT_FOUND}), 404

        query = """
            SELECT id, rating, title, content, spoiler_warning, created_at, updated_at
            FROM reviews
            WHERE book_id = %s
        """

        reviews = db.execute_query(query, [book_id], fetch_all=True)

        return jsonify({"status": "success", "count": len(reviews), "data": reviews})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@reviews_bp.route("/<int:book_id>/reviews", methods=["POST"])
def create_or_update_review(book_id):
    """Create or update review for a book."""
    try:
        data = request.get_json() or {}

        # Validate
        valid, msg = validate_review_data(data)
        if valid is not True:
            return jsonify({"status": "error", "message": "Validation failed", "errors": msg}), 400

        db = get_db()

        # Check book exists
        check_query = "SELECT id FROM books WHERE id = %s"
        if not db.execute_query(check_query, [book_id], fetch_one=True):
            return jsonify({"status": "error", "message": ErrorMessages.BOOK_NOT_FOUND}), 404

        # Check if review exists
        review_check = "SELECT id FROM reviews WHERE book_id = %s"
        existing_review = db.execute_query(review_check, [book_id], fetch_one=True)

        if existing_review:
            # Update existing review
            query = """
                UPDATE reviews
                SET rating = %s,
                    title = %s,
                    content = %s,
                    spoiler_warning = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE book_id = %s
            """

            params = [
                data["rating"],
                data.get("title"),
                data["content"],
                data.get("spoiler_warning", False),
                book_id,
            ]

            db.execute_update(query, params)
            return jsonify({"status": "success", "message": "Review updated successfully"})
        else:
            # Create new review
            query = """
                INSERT INTO reviews (book_id, rating, title, content, spoiler_warning, created_at)
                VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                RETURNING id
            """

            params = [
                book_id,
                data["rating"],
                data.get("title"),
                data["content"],
                data.get("spoiler_warning", False),
            ]

            review_id = db.execute_insert(query, params)
            return (
                jsonify(
                    {
                        "status": "success",
                        "message": "Review created successfully",
                        "id": review_id,
                    }
                ),
                201,
            )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@reviews_bp.route("/<int:book_id>/reviews", methods=["DELETE"])
def delete_review(book_id):
    """Delete review for a book."""
    try:
        db = get_db()

        # Check book exists
        check_query = "SELECT id FROM books WHERE id = %s"
        if not db.execute_query(check_query, [book_id], fetch_one=True):
            return jsonify({"status": "error", "message": ErrorMessages.BOOK_NOT_FOUND}), 404

        # Delete review
        query = "DELETE FROM reviews WHERE book_id = %s"
        db.execute_update(query, [book_id])

        return jsonify({"status": "success", "message": "Review deleted successfully"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
