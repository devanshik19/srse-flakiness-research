import pytest
from django.contrib.auth.models import User
from django.db.backends.base.operations import BaseDatabaseOperations
from django.core.management.color import no_style
from django.db import connection, transaction

class CustomDatabaseOperations(BaseDatabaseOperations):
    def sql_flush(self, style, tables, *, reset_sequences=False, allow_cascade=False):
        sql_statements = []
        for table in tables:
            sql_statements.append(f'TRUNCATE TABLE {table};')
            if reset_sequences:
                sql_statements.append(f'ALTER SEQUENCE {table}_id_seq RESTART WITH 1;')
        return sql_statements

@pytest.fixture
def custom_db_operations():
    return CustomDatabaseOperations(connection)

def test_sql_flush_no_sequences(custom_db_operations):
    tables = ['auth_user']
    sql_statements = custom_db_operations.sql_flush(no_style(), tables)

    assert sql_statements == [
        'TRUNCATE TABLE auth_user;'
    ]

def test_sql_flush_with_sequences(custom_db_operations):
    tables = ['auth_user']
    sql_statements = custom_db_operations.sql_flush(no_style(), tables, reset_sequences=True)

    assert sql_statements == [
        'TRUNCATE TABLE auth_user;',
        'ALTER SEQUENCE auth_user_id_seq RESTART WITH 1;'
    ]

def test_sql_flush_with_cascade(custom_db_operations):
    tables = ['auth_user']
    sql_statements = custom_db_operations.sql_flush(no_style(), tables, reset_sequences=True, allow_cascade=True)

    assert sql_statements == [
        'TRUNCATE TABLE auth_user;',
        'ALTER SEQUENCE auth_user_id_seq RESTART WITH 1;'
    ]