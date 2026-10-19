import pytest
from django.contrib.auth.models import User
from django.db.backends.base.operations import BaseDatabaseOperations

class TestBaseDatabaseOperations(BaseDatabaseOperations):
    def sql_flush(self, style, tables, *, reset_sequences=False, allow_cascade=False):
        flush_commands = []
        for table in tables:
            command = f'TRUNCATE TABLE {table}'
            if allow_cascade:
                command += ' CASCADE'
            flush_commands.append(command)
            if reset_sequences:
                flush_commands.append(f'ALTER SEQUENCE {table}_id_seq RESTART WITH 1;')
        return flush_commands

@pytest.fixture
def db_operations():
    return TestBaseDatabaseOperations(None)

def test_sql_flush_with_cascade(db_operations):
    tables = ['auth_user']
    result = db_operations.sql_flush(None, tables, reset_sequences=False, allow_cascade=True)
    expected = [
        'TRUNCATE TABLE auth_user CASCADE'
    ]
    assert result == expected

def test_sql_flush_without_cascade(db_operations):
    tables = ['auth_user']
    result = db_operations.sql_flush(None, tables, reset_sequences=False, allow_cascade=False)
    expected = [
        'TRUNCATE TABLE auth_user'
    ]
    assert result == expected

def test_sql_flush_with_reset_sequences(db_operations):
    tables = ['auth_user']
    result = db_operations.sql_flush(None, tables, reset_sequences=True, allow_cascade=False)
    expected = [
        'TRUNCATE TABLE auth_user',
        'ALTER SEQUENCE auth_user_id_seq RESTART WITH 1;'
    ]
    assert result == expected

def test_sql_flush_with_reset_sequences_and_cascade(db_operations):
    tables = ['auth_user']
    result = db_operations.sql_flush(None, tables, reset_sequences=True, allow_cascade=True)
    expected = [
        'TRUNCATE TABLE auth_user CASCADE',
        'ALTER SEQUENCE auth_user_id_seq RESTART WITH 1;'
    ]
    assert result == expected