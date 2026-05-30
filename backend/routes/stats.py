"""Statistics and analytics endpoints."""
from flask import jsonify
from routes import stats_bp
from db import get_db


@stats_bp.route("/stats", methods=["GET"])
def get_stats():
    """Get reading statistics and library overview."""
    try:
        db = get_db()

        # Total books
        total_query = "SELECT COUNT(*) as count FROM books"
        total = db.execute_query(total_query, fetch_one=True)

        # Books by status
        status_query = """
            SELECT bs.status, COUNT(*) as count
            FROM book_status bs
            GROUP BY bs.status
        """
        by_status = db.execute_query(status_query, fetch_all=True)

        # Books by genre
        genre_query = """
            SELECT genre, COUNT(*) as count
            FROM books b, LATERAL UNNEST(b.genre) as genre
            GROUP BY genre
            ORDER BY count DESC
        """
        by_genre = db.execute_query(genre_query, fetch_all=True)

        # Books by rating
        rating_query = """
            SELECT bs.rating, COUNT(*) as count
            FROM book_status bs
            WHERE bs.rating IS NOT NULL
            GROUP BY bs.rating
            ORDER BY bs.rating DESC
        """
        by_rating = db.execute_query(rating_query, fetch_all=True)

        # Average rating
        avg_rating_query = """
            SELECT ROUND(AVG(bs.rating)::numeric, 2) as average_rating,
                   COUNT(*) as reviewed_books
            FROM book_status bs
            WHERE bs.rating IS NOT NULL
        """
        avg_rating = db.execute_query(avg_rating_query, fetch_one=True)

        # Pages read statistics
        pages_query = """
            SELECT COUNT(*) as total_books_read,
                   SUM(bs.pages_read) as total_pages_started,
                   ROUND(AVG(b.pages)::numeric, 1) as average_book_length
            FROM book_status bs
            JOIN books b ON bs.book_id = b.id
            WHERE bs.status IN ('reading', 'completed')
        """
        pages_stats = db.execute_query(pages_query, fetch_one=True)

        # Top authors
        top_authors_query = """
            SELECT a.name, COUNT(*) as count
            FROM books b
            JOIN authors a ON b.author_id = a.id
            GROUP BY a.id, a.name
            ORDER BY count DESC
            LIMIT 5
        """
        top_authors = db.execute_query(top_authors_query, fetch_all=True)

        return jsonify(
            {
                "status": "success",
                "data": {
                    "total_books": total.get("count") if total else 0,
                    "by_status": by_status,
                    "by_genre": by_genre,
                    "by_rating": by_rating,
                    "average_rating": avg_rating,
                    "pages_statistics": pages_stats,
                    "top_authors": top_authors,
                },
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
