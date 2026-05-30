"""Flask application factory."""
from flask import Flask, jsonify
from flask_cors import CORS
from config import get_config
from db import init_db
from services import init_container
from routes import books_bp, book_status_bp, reviews_bp, tbr_bp, stats_bp


def create_app(config=None):
    """Create and configure Flask application."""
    app = Flask(__name__)

    # Load configuration
    if config is None:
        config = get_config()
    app.config.from_object(config)

    # Initialize database
    init_db(app)

    # Initialize service container (dependency injection)
    container = init_container()
    app.container = container

    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register blueprints
    app.register_blueprint(books_bp)
    app.register_blueprint(book_status_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(tbr_bp)
    app.register_blueprint(stats_bp)

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return jsonify({"error": "Not found", "status": 404}), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        return jsonify({"error": "Internal server error", "status": 500}), 500

    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 errors."""
        return jsonify({"error": "Bad request", "status": 400}), 400

    # Health check endpoint
    @app.route("/api/health", methods=["GET"])
    def health_check():
        """Health check endpoint."""
        return jsonify({"status": "healthy", "message": "Library API is running"})

    # Root endpoint
    @app.route("/api", methods=["GET"])
    def api_info():
        """API information endpoint."""
        return jsonify(
            {
                "name": "Personal Library API",
                "version": "1.0.0",
                "description": "RESTful API for managing a personal book library",
                "endpoints": {
                    "books": "/api/books",
                    "book_status": "/api/books/{id}/status",
                    "reviews": "/api/books/{id}/reviews",
                    "tbr": "/api/tbr",
                    "stats": "/api/stats",
                    "health": "/api/health",
                },
            }
        )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
