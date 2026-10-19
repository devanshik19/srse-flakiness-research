import pytest
from django.db.backends.sqlite3.features import DatabaseFeatures
from django.contrib.auth.models import User
from django.db import connection
from unittest.mock import patch

def test_django_test_skips():
    db_features = DatabaseFeatures()

    # Patch connection properties for testing various scenarios
    with patch.object(db_features.connection, 'is_in_memory_db', return_value=False), \
         patch.object(Database, 'sqlite_version_info', (3, 26)):
        skips = db_features.django_test_skips()
        assert 'Nondeterministic failure on SQLite < 3.27.' in skips
        assert 'model_fields.test_integerfield.PositiveIntegerFieldTests.test_negative_values' in skips[
            "SQLite doesn't have a constraint."]

    with patch.object(db_features.connection, 'is_in_memory_db', return_value=True), \
         patch.object(Database, 'sqlite_version_info', (3, 28)):
        skips = db_features.django_test_skips()
        assert "the sqlite backend's close() method is a no-op when using an in-memory database" in skips

    with patch.object(db_features.connection, 'is_in_memory_db', return_value=False), \
         patch.object(Database, 'sqlite_version_info', (3, 28)):
        skips = db_features.django_test_skips()
        assert 'Nondeterministic failure on SQLite < 3.27.' not in skips
        assert len(skips) > 0  # there should still be some skips

    assert 'SQLite stores values rounded to 15 significant digits.' in skips
    assert 'SQLite naively remakes the table on field alteration.' in skips
    assert "SQLite doesn't support negative precision for ROUND()." in skips