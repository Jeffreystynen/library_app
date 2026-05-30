"""Service Container - Dependency Injection for all services."""
from services.database_service import DatabaseService


class ServiceContainer:
    """Dependency Injection container for services."""

    def __init__(self):
        """Initialize all services as singletons."""
        self._services = {}
        self._initialize_services()

    def _initialize_services(self):
        """Initialize all services."""
        self._services["database"] = DatabaseService()

    @property
    def database(self) -> DatabaseService:
        """Get database service."""
        return self._services["database"]

    def get_service(self, name: str):
        """Get service by name."""
        return self._services.get(name)

    def register_service(self, name: str, service):
        """Register a custom service (useful for testing)."""
        self._services[name] = service

    def reset(self):
        """Reset all services (useful for testing)."""
        self._initialize_services()


# Global container instance
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
