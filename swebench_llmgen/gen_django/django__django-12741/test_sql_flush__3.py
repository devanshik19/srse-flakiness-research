import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.core.management.color import no_style
from django.db.backends.base.operations import BaseDatabaseOperations

class TestBaseDatabaseOperations(BaseDatabaseOperations):
    def sql_flush(self, style, tables, *, reset_sequences=False, allow_cascade=False):
        # Simple implementation for testing purposes
        sql_statements = []
        for table in tables:
            sql_statements.append(f"DELETE FROM {style.quote_name(table)}")
            if reset_sequences:
                sql_statements.append(f"ALTER SEQUENCE {style.quote_name(table)}_id_seq RESTART WITH 1")
        return sql_statements

@pytest.fixture
def sample_user():
    return User.objects.create(username='testuser')

def test_sql_flush_reset_sequences(sample_user):
    ops = TestBaseDatabaseOperations(connection)
    tables = ['auth_user']
    expected_sql = [
        "DELETE FROM auth_user",
        "ALTER SEQUENCE auth_user_id_seq RESTART WITH 1"
    ]
    result = ops.sql_flush(no_style(), tables, reset_sequences=True)
    assert result == expected_sql

def test_sql_flush_no_reset_sequences(sample_user):
    ops = TestBaseDatabaseOperations(connection)
    tables = ['auth_user']
    expected_sql = [
        "DELETE FROM auth_user"
    ]
    result = ops.sql_flush(no_style(), tables, reset_sequences=False)
    assert result == expected_sql

def test_sql_flush_multiple_tables():
    ops = TestBaseDatabaseOperations(connection)
    tables = ['auth_user', 'auth_group']
    expected_sql = [
        "DELETE FROM auth_user",
        "DELETE FROM auth_group",
        "ALTER SEQUENCE auth_user_id_seq RESTART WITH 1",
        "ALTER SEQUENCE auth_group_id_seq RESTART WITH 1"
    ]
    result = ops.sql_flush(no_style(), tables, reset_sequences=True)
    assert result == expected_sql