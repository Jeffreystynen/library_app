"""Base repository class for all data access."""
from abc import ABC, abstractmethod
from db import get_db


class BaseRepository(ABC):
    """Abstract base class for all repositories."""

    def __init__(self):
        """Initialize repository with database instance."""
        self.db = get_db()

    def execute_query(self, query, params=None, fetch_one=False, fetch_all=True):
        """Execute a SELECT query."""
        return self.db.execute_query(query, params, fetch_one, fetch_all)

    def execute_update(self, query, params=None):
        """Execute an INSERT, UPDATE, or DELETE query."""
        return self.db.execute_update(query, params)

    def execute_insert(self, query, params=None):
        """Execute an INSERT query and return the ID of inserted row."""
        return self.db.execute_insert(query, params)

    @abstractmethod
    def find_by_id(self, id):
        """Find a record by ID. Must be implemented by subclasses."""
        pass

    @abstractmethod
    def find_all(self):
        """Find all records. Must be implemented by subclasses."""
        pass
