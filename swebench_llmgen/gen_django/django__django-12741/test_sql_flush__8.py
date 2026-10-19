import pytest
from django.core.management.color import no_style
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.base.operations import BaseDatabaseOperations


class MockDatabaseOperations(BaseDatabaseOperations):
    def sql_flush(self, style, tables, *, reset_sequences=False, allow_cascade=False):
        # Mock implementation for testing purposes
        sql_statements = [f"TRUNCATE TABLE {table}" for table in tables]
        if reset_sequences:
            sql_statements.append("ALTER SEQUENCE auth_user_id_seq RESTART WITH 1")
        return sql_statements


@pytest.fixture
def mock_db_operations():
    return MockDatabaseOperations(connection)


def test_sql_flush_no_reset_sequences(mock_db_operations):
    tables = ['auth_user']
    result = mock_db_operations.sql_flush(no_style(), tables)
    expected = ["TRUNCATE TABLE auth_user"]
    assert result == expected


def test_sql_flush_with_reset_sequences(mock_db_operations):
    tables = ['auth_user']
    result = mock_db_operations.sql_flush(no_style(), tables, reset_sequences=True)
    expected = ["TRUNCATE TABLE auth_user", "ALTER SEQUENCE auth_user_id_seq RESTART WITH 1"]
    assert result == expected


def test_sql_flush_with_allow_cascade(mock_db_operations):
    tables = ['auth_user']
    result = mock_db_operations.sql_flush(no_style(), tables, reset_sequences=True, allow_cascade=True)
    expected = ["TRUNCATE TABLE auth_user", "ALTER SEQUENCE auth_user_id_seq RESTART WITH 1"]
    assert result == expected