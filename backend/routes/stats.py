"""Statistics and analytics endpoints."""
from flask import jsonify, current_app
from routes import stats_bp


def get_service():
    """Get database service from app container (DI)."""
    return current_app.container.database


@stats_bp.route("/stats", methods=["GET"])
def get_stats():
    """Get reading statistics and library overview."""
    try:
        service = get_service()
        stats = service.get_all_stats()

        return jsonify(
            {
                "status": "success",
                "data": stats,
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
