"""To-Be-Read (TBR) list endpoints."""
from flask import request, jsonify
from routes import tbr_bp
from db import get_db
from utils.constants import ErrorMessages


@tbr_bp.route("", methods=["GET"])
def get_tbr_list():
    """Get all books in TBR list with priority ordering."""
    try:
        db = get_db()

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

        items = db.execute_query(query, fetch_all=True)

        return jsonify({"status": "success", "count": len(items), "data": items})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@tbr_bp.route("/<int:book_id>", methods=["POST"])
def add_to_tbr(book_id):
    """Add a book to the TBR list."""
    try:
        data = request.get_json() or {}
        priority = data.get("priority", 0)

        db = get_db()

        # Check book exists
        check_query = "SELECT id FROM books WHERE id = %s"
        if not db.execute_query(check_query, [book_id], fetch_one=True):
            return jsonify({"status": "error", "message": ErrorMessages.BOOK_NOT_FOUND}), 404

        # Check if already in TBR
        tbr_check = "SELECT id FROM tbr_items WHERE book_id = %s"
        if db.execute_query(tbr_check, [book_id], fetch_one=True):
            return (
                jsonify({"status": "error", "message": "Book is already in TBR list"}),
                400,
            )

        # Get default TBR list (id=1)
        tbr_list_query = "SELECT id FROM tbr_list LIMIT 1"
        tbr_list = db.execute_query(tbr_list_query, fetch_one=True)

        if not tbr_list:
            # Create default TBR list if it doesn't exist
            create_tbr = "INSERT INTO tbr_list (name, description) VALUES ('My Reading List', 'Books I want to read') RETURNING id"
            tbr_list_id = db.execute_insert(create_tbr, [])
        else:
            tbr_list_id = tbr_list["id"]

        # Add to TBR list
        query = """
            INSERT INTO tbr_items (tbr_list_id, book_id, priority)
            VALUES (%s, %s, %s)
            RETURNING id
        """

        item_id = db.execute_insert(query, [tbr_list_id, book_id, priority])

        # Update book_status to mark as TBR
        status_query = "UPDATE book_status SET is_tbr = TRUE WHERE book_id = %s"
        db.execute_update(status_query, [book_id])

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Book added to TBR list",
                    "id": item_id,
                }
            ),
            201,
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@tbr_bp.route("/<int:book_id>", methods=["DELETE"])
def remove_from_tbr(book_id):
    """Remove a book from the TBR list."""
    try:
        db = get_db()

        # Check book exists
        check_query = "SELECT id FROM books WHERE id = %s"
        if not db.execute_query(check_query, [book_id], fetch_one=True):
            return jsonify({"status": "error", "message": ErrorMessages.BOOK_NOT_FOUND}), 404

        # Remove from TBR list
        query = "DELETE FROM tbr_items WHERE book_id = %s"
        db.execute_update(query, [book_id])

        # Update book_status to mark as not TBR
        status_query = "UPDATE book_status SET is_tbr = FALSE WHERE book_id = %s"
        db.execute_update(status_query, [book_id])

        return jsonify({"status": "success", "message": "Book removed from TBR list"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@tbr_bp.route("/order", methods=["PUT"])
def reorder_tbr():
    """Reorder TBR list items by priority."""
    try:
        data = request.get_json() or {}

        if "items" not in data or not isinstance(data["items"], list):
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "items field must be a list of items with id and priority",
                    }
                ),
                400,
            )

        db = get_db()

        # Update priorities
        for item in data["items"]:
            if "id" not in item or "priority" not in item:
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": "Each item must have id and priority",
                        }
                    ),
                    400,
                )

            query = "UPDATE tbr_items SET priority = %s WHERE id = %s"
            db.execute_update(query, [item["priority"], item["id"]])

        return jsonify({"status": "success", "message": "TBR list reordered successfully"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
