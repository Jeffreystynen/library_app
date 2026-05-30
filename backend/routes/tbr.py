"""To-Be-Read (TBR) list endpoints."""
from flask import request, jsonify, current_app
from routes import tbr_bp


def get_service():
    """Get database service from app container (DI)."""
    return current_app.container.database


@tbr_bp.route("", methods=["GET"])
def get_tbr_list():
    """Get all books in TBR list with priority ordering."""
    try:
        service = get_service()
        items = service.get_tbr_list()
        return jsonify({"status": "success", "count": len(items) if items else 0, "data": items or []})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@tbr_bp.route("/<int:book_id>", methods=["POST"])
def add_to_tbr(book_id):
    """Add a book to the TBR list."""
    try:
        data = request.get_json() or {}
        service = get_service()
        item_id = service.add_to_tbr(book_id, priority=data.get("priority", 0))

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

    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@tbr_bp.route("/<int:book_id>", methods=["DELETE"])
def remove_from_tbr(book_id):
    """Remove a book from the TBR list."""
    try:
        service = get_service()
        service.remove_from_tbr(book_id)

        return jsonify({"status": "success", "message": "Book removed from TBR list"})

    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@tbr_bp.route("/order", methods=["PUT"])
def reorder_tbr():
    """Reorder TBR list items by priority."""
    try:
        data = request.get_json() or {}
        service = get_service()
        service.reorder_tbr(data.get("items", []))

        return jsonify({"status": "success", "message": "TBR list reordered successfully"})

    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
