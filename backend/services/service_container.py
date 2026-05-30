"""Service container for dependency injection."""
from services.book_repository import BookRepository
from services.book_status_repository import BookStatusRepository
from services.review_repository import ReviewRepository
from services.tbr_repository import TBRRepository
from services.stats_repository import StatsRepository


class ServiceContainer:
    """Container for managing all service dependencies."""

    def __init__(self):
        """Initialize service container with all repositories."""
        self._repositories = {}
        self._initialize_repositories()

    def _initialize_repositories(self):
        """Initialize all repositories as singletons."""
        self._repositories["book"] = BookRepository()
        self._repositories["book_status"] = BookStatusRepository()
        self._repositories["review"] = ReviewRepository()
        self._repositories["tbr"] = TBRRepository()
        self._repositories["stats"] = StatsRepository()

    @property
    def book(self) -> BookRepository:
        """Get book repository."""
        return self._repositories["book"]

    @property
    def book_status(self) -> BookStatusRepository:
        """Get book status repository."""
        return self._repositories["book_status"]

    @property
    def review(self) -> ReviewRepository:
        """Get review repository."""
        return self._repositories["review"]

    @property
    def tbr(self) -> TBRRepository:
        """Get TBR repository."""
        return self._repositories["tbr"]

    @property
    def stats(self) -> StatsRepository:
        """Get stats repository."""
        return self._repositories["stats"]

    def get_repository(self, name: str):
        """Get repository by name."""
        return self._repositories.get(name)

    def register_repository(self, name: str, repository):
        """Register a custom repository (useful for testing)."""
        self._repositories[name] = repository

    def reset(self):
        """Reset all repositories (useful for testing)."""
        self._initialize_repositories()


# Global service container instance
_container = None


def init_container():
    """Initialize the global service container."""
    global _container
    _container = ServiceContainer()
    return _container


def get_container() -> ServiceContainer:
    """Get the global service container."""
    global _container
    if _container is None:
        _container = init_container()
    return _container
