"""API routes package."""
from flask import Blueprint

# Create blueprints
books_bp = Blueprint("books", __name__, url_prefix="/api/books")
book_status_bp = Blueprint("book_status", __name__, url_prefix="/api/books")
reviews_bp = Blueprint("reviews", __name__, url_prefix="/api/books")
tbr_bp = Blueprint("tbr", __name__, url_prefix="/api/tbr")
stats_bp = Blueprint("stats", __name__, url_prefix="/api")

# Import route handlers to register them with blueprints
from . import books  # noqa
from . import book_status  # noqa
from . import reviews  # noqa
from . import tbr  # noqa
from . import stats  # noqa

__all__ = [
    "books_bp",
    "book_status_bp",
    "reviews_bp",
    "tbr_bp",
    "stats_bp",
]
