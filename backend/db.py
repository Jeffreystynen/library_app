"""Database connection and query utilities."""
import psycopg2
import psycopg2.extras
from contextlib import contextmanager
from config import Config


class Database:
    """Database connection manager."""

    def __init__(self, config):
        """Initialize database with config."""
        self.config = config
        self.connection_params = {
            "host": config.DB_HOST,
            "port": config.DB_PORT,
            "database": config.DB_NAME,
            "user": config.DB_USER,
            "password": config.DB_PASSWORD,
        }

    def connect(self):
        """Create a new database connection."""
        try:
            conn = psycopg2.connect(**self.connection_params)
            return conn
        except psycopg2.Error as e:
            raise Exception(f"Database connection failed: {e}")

    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = self.connect()
        try:
            yield conn
        finally:
            conn.close()

    @contextmanager
    def get_cursor(self, commit=False, dict_cursor=True):
        """Context manager for database cursors."""
        with self.get_connection() as conn:
            cursor_factory = psycopg2.extras.RealDictCursor if dict_cursor else None
            cur = conn.cursor(cursor_factory=cursor_factory)
            try:
                yield cur
                if commit:
                    conn.commit()
            except psycopg2.Error as e:
                conn.rollback()
                raise Exception(f"Database error: {e}")
            finally:
                cur.close()

    def execute_query(self, query, params=None, fetch_one=False, fetch_all=True):
        """Execute a SELECT query and return results."""
        with self.get_cursor(dict_cursor=True) as cur:
            cur.execute(query, params or [])

            if fetch_one:
                return cur.fetchone()
            elif fetch_all:
                return cur.fetchall()
            else:
                return cur

    def execute_update(self, query, params=None):
        """Execute INSERT, UPDATE, or DELETE query."""
        with self.get_cursor(commit=True) as cur:
            cur.execute(query, params or [])
            return cur.rowcount

    def execute_insert(self, query, params=None):
        """Execute INSERT query and return inserted ID."""
        with self.get_cursor(commit=True) as cur:
            cur.execute(query, params or [])
            result = cur.fetchone()
            return result[0] if result else None


# Global database instance
db = None


def init_db(app):
    """Initialize database with Flask app."""
    global db
    db = Database(app.config)
    return db


def get_db():
    """Get the global database instance."""
    if db is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return db
