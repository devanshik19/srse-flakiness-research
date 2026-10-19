import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.sqlite3.features import DatabaseFeatures
from .base import Database

@pytest.mark.django_db
def test_django_test_skips():
    features = DatabaseFeatures()

    # Mock the Database.sqlite_version_info for the test
    original_sqlite_version_info = Database.sqlite_version_info
    Database.sqlite_version_info = (3, 20)  # Mocking an older version

    # Mock the connection as if it is in-memory
    class MockConnection:
        @staticmethod
        def is_in_memory_db():
            return True

    # Replace the connection on the features instance
    features.connection = MockConnection()

    skips = features.django_test_skips()

    # Validate the contents of the skips
    assert 'SQLite stores values rounded to 15 significant digits.' in skips
    assert 'SQLite naively remakes the table on field alteration.' in skips
    assert "SQLite doesn't have a constraint." in skips
    assert "SQLite doesn't support negative precision for ROUND()." in skips
    assert 'Nondeterministic failure on SQLite < 3.27.' in skips  # Due to mocked version info
    assert "the sqlite backend's close() method is a no-op when using an in-memory database" in skips

    # Clean up
    Database.sqlite_version_info = original_sqlite_version_info