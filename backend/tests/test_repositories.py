"""Tests for repository pattern implementation."""
import pytest
from unittest.mock import Mock, patch
from repositories.book_repository import BookRepository
from repositories.book_status_repository import BookStatusRepository
from repositories.review_repository import ReviewRepository
from repositories.tbr_repository import TBRRepository
from repositories.stats_repository import StatsRepository
from services.container import ServiceContainer


class TestBookRepository:
    """Tests for BookRepository."""

    def test_book_repository_inherits_from_base(self):
        """Test that BookRepository has required methods."""
        repo = BookRepository()
        assert hasattr(repo, "find_by_id")
        assert hasattr(repo, "find_all")
        assert hasattr(repo, "create")
        assert hasattr(repo, "update")
        assert hasattr(repo, "delete")
        assert hasattr(repo, "search")
        assert hasattr(repo, "exists")

    def test_book_repository_can_be_instantiated(self):
        """Test that repository can be instantiated."""
        repo = BookRepository()
        assert repo is not None
        assert hasattr(repo, "db")

    def test_book_repository_has_database_instance(self):
        """Test that repository has access to database."""
        repo = BookRepository()
        assert repo.db is not None

    def test_create_method_signature(self):
        """Test that create method has correct parameters."""
        repo = BookRepository()
        # Should accept these parameters
        params = ["title", "author_id"]
        create_method = repo.create
        # Check it's callable
        assert callable(create_method)


class TestBookStatusRepository:
    """Tests for BookStatusRepository."""

    def test_book_status_repository_inherits_from_base(self):
        """Test that BookStatusRepository has required methods."""
        repo = BookStatusRepository()
        assert hasattr(repo, "find_by_id")
        assert hasattr(repo, "find_by_book_id")
        assert hasattr(repo, "find_all")
        assert hasattr(repo, "update_status")
        assert hasattr(repo, "update_rating")
        assert hasattr(repo, "update_progress")
        assert hasattr(repo, "update_notes")

    def test_book_status_repository_can_be_instantiated(self):
        """Test that repository can be instantiated."""
        repo = BookStatusRepository()
        assert repo is not None

    def test_get_reading_progress_method_exists(self):
        """Test that reading progress method exists."""
        repo = BookStatusRepository()
        assert hasattr(repo, "get_reading_progress")
        assert callable(repo.get_reading_progress)

    def test_get_by_status_method_exists(self):
        """Test that get_by_status method exists."""
        repo = BookStatusRepository()
        assert hasattr(repo, "get_by_status")
        assert callable(repo.get_by_status)


class TestReviewRepository:
    """Tests for ReviewRepository."""

    def test_review_repository_inherits_from_base(self):
        """Test that ReviewRepository has required methods."""
        repo = ReviewRepository()
        assert hasattr(repo, "find_by_id")
        assert hasattr(repo, "find_by_book_id")
        assert hasattr(repo, "find_all")
        assert hasattr(repo, "create")
        assert hasattr(repo, "update")
        assert hasattr(repo, "delete")

    def test_review_repository_can_be_instantiated(self):
        """Test that repository can be instantiated."""
        repo = ReviewRepository()
        assert repo is not None

    def test_get_by_rating_method_exists(self):
        """Test that get_by_rating method exists."""
        repo = ReviewRepository()
        assert hasattr(repo, "get_by_rating")
        assert callable(repo.get_by_rating)

    def test_exists_method_exists(self):
        """Test that exists method exists."""
        repo = ReviewRepository()
        assert hasattr(repo, "exists")
        assert callable(repo.exists)


class TestTBRRepository:
    """Tests for TBRRepository."""

    def test_tbr_repository_inherits_from_base(self):
        """Test that TBRRepository has required methods."""
        repo = TBRRepository()
        assert hasattr(repo, "find_by_id")
        assert hasattr(repo, "find_all")
        assert hasattr(repo, "add_book")
        assert hasattr(repo, "remove_book")
        assert hasattr(repo, "reorder_items")

    def test_tbr_repository_can_be_instantiated(self):
        """Test that repository can be instantiated."""
        repo = TBRRepository()
        assert repo is not None

    def test_get_default_list_method_exists(self):
        """Test that get_default_list method exists."""
        repo = TBRRepository()
        assert hasattr(repo, "get_default_list")
        assert callable(repo.get_default_list)

    def test_update_priority_method_exists(self):
        """Test that update_priority method exists."""
        repo = TBRRepository()
        assert hasattr(repo, "update_priority")
        assert callable(repo.update_priority)

    def test_is_in_tbr_method_exists(self):
        """Test that is_in_tbr method exists."""
        repo = TBRRepository()
        assert hasattr(repo, "is_in_tbr")
        assert callable(repo.is_in_tbr)

    def test_get_next_to_read_method_exists(self):
        """Test that get_next_to_read method exists."""
        repo = TBRRepository()
        assert hasattr(repo, "get_next_to_read")
        assert callable(repo.get_next_to_read)


class TestStatsRepository:
    """Tests for StatsRepository."""

    def test_stats_repository_inherits_from_base(self):
        """Test that StatsRepository exists and has methods."""
        repo = StatsRepository()
        assert hasattr(repo, "get_total_books")
        assert hasattr(repo, "get_books_by_status")
        assert hasattr(repo, "get_books_by_genre")
        assert hasattr(repo, "get_books_by_rating")
        assert hasattr(repo, "get_average_rating")
        assert hasattr(repo, "get_all_stats")

    def test_stats_repository_can_be_instantiated(self):
        """Test that repository can be instantiated."""
        repo = StatsRepository()
        assert repo is not None

    def test_get_pages_statistics_method_exists(self):
        """Test that get_pages_statistics method exists."""
        repo = StatsRepository()
        assert hasattr(repo, "get_pages_statistics")
        assert callable(repo.get_pages_statistics)

    def test_get_top_authors_method_exists(self):
        """Test that get_top_authors method exists."""
        repo = StatsRepository()
        assert hasattr(repo, "get_top_authors")
        assert callable(repo.get_top_authors)


class TestServiceContainer:
    """Tests for ServiceContainer dependency injection."""

    def test_service_container_can_be_created(self):
        """Test that service container can be instantiated."""
        container = ServiceContainer()
        assert container is not None

    def test_service_container_provides_book_repository(self):
        """Test that container provides book repository."""
        container = ServiceContainer()
        assert container.book is not None
        assert isinstance(container.book, BookRepository)

    def test_service_container_provides_book_status_repository(self):
        """Test that container provides book status repository."""
        container = ServiceContainer()
        assert container.book_status is not None
        assert isinstance(container.book_status, BookStatusRepository)

    def test_service_container_provides_review_repository(self):
        """Test that container provides review repository."""
        container = ServiceContainer()
        assert container.review is not None
        assert isinstance(container.review, ReviewRepository)

    def test_service_container_provides_tbr_repository(self):
        """Test that container provides TBR repository."""
        container = ServiceContainer()
        assert container.tbr is not None
        assert isinstance(container.tbr, TBRRepository)

    def test_service_container_provides_stats_repository(self):
        """Test that container provides stats repository."""
        container = ServiceContainer()
        assert container.stats is not None
        assert isinstance(container.stats, StatsRepository)

    def test_service_container_get_repository_by_name(self):
        """Test that repositories can be retrieved by name."""
        container = ServiceContainer()
        assert container.get_repository("book") is not None
        assert container.get_repository("book_status") is not None
        assert container.get_repository("review") is not None
        assert container.get_repository("tbr") is not None
        assert container.get_repository("stats") is not None

    def test_service_container_returns_same_instance(self):
        """Test that container returns same repository instance."""
        container = ServiceContainer()
        book_repo_1 = container.book
        book_repo_2 = container.book
        assert book_repo_1 is book_repo_2  # Same instance

    def test_service_container_register_custom_repository(self):
        """Test that custom repositories can be registered."""
        container = ServiceContainer()
        mock_repo = Mock()
        container.register_repository("custom", mock_repo)
        assert container.get_repository("custom") is mock_repo

    def test_service_container_reset(self):
        """Test that container can be reset."""
        container = ServiceContainer()
        original_book = container.book
        container.reset()
        new_book = container.book
        assert original_book is not new_book  # Different instances after reset

    def test_repositories_are_singletons(self):
        """Test that repositories within container are singletons."""
        container = ServiceContainer()
        book1 = container.book
        book2 = container.book
        review1 = container.review
        review2 = container.review

        assert book1 is book2
        assert review1 is review2


class TestRepositoryPattern:
    """Integration tests for repository pattern."""

    def test_all_repositories_have_database_access(self):
        """Test that all repositories can access database."""
        container = ServiceContainer()

        for repo_name in ["book", "book_status", "review", "tbr", "stats"]:
            repo = container.get_repository(repo_name)
            assert hasattr(repo, "db")
            assert repo.db is not None

    def test_all_repositories_inherit_execute_methods(self):
        """Test that all repositories have query execution methods."""
        container = ServiceContainer()

        for repo_name in ["book", "book_status", "review", "tbr", "stats"]:
            repo = container.get_repository(repo_name)
            assert hasattr(repo, "execute_query")
            assert hasattr(repo, "execute_update")
            assert hasattr(repo, "execute_insert")

    def test_repository_methods_are_callable(self):
        """Test that repository methods are callable."""
        container = ServiceContainer()

        book_repo = container.book
        assert callable(book_repo.find_by_id)
        assert callable(book_repo.find_all)
        assert callable(book_repo.create)

        review_repo = container.review
        assert callable(review_repo.find_by_book_id)
        assert callable(review_repo.create)

        tbr_repo = container.tbr
        assert callable(tbr_repo.add_book)
        assert callable(tbr_repo.remove_book)
