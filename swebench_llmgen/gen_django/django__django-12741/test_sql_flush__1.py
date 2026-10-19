import pytest
from django.core.management.color import no_style
from django.contrib.auth.models import User
from django.db.backends.base.operations import BaseDatabaseOperations


class TestBaseDatabaseOperations(BaseDatabaseOperations):
    def sql_flush(self, style, tables, *, reset_sequences=False, allow_cascade=False):
        # Mock implementation just for testing purposes
        sql_statements = [f"TRUNCATE TABLE {table}" for table in tables]
        if reset_sequences:
            sql_statements.extend([f"ALTER TABLE {table} ALTER COLUMN id RESTART WITH 1" for table in tables])
        return sql_statements


def test_sql_flush_no_reset_sequences():
    db_ops = TestBaseDatabaseOperations()
    tables = ['auth_user', 'auth_group']
    sql_statements = db_ops.sql_flush(no_style(), tables, reset_sequences=False, allow_cascade=False)
    
    assert len(sql_statements) == 2
    assert "TRUNCATE TABLE auth_user" in sql_statements
    assert "TRUNCATE TABLE auth_group" in sql_statements


def test_sql_flush_with_reset_sequences():
    db_ops = TestBaseDatabaseOperations()
    tables = ['auth_user', 'auth_group']
    sql_statements = db_ops.sql_flush(no_style(), tables, reset_sequences=True, allow_cascade=False)
    
    assert len(sql_statements) == 4
    assert "TRUNCATE TABLE auth_user" in sql_statements
    assert "ALTER TABLE auth_user ALTER COLUMN id RESTART WITH 1" in sql_statements
    assert "TRUNCATE TABLE auth_group" in sql_statements
    assert "ALTER TABLE auth_group ALTER COLUMN id RESTART WITH 1" in sql_statements


def test_sql_flush_allow_cascade():
    db_ops = TestBaseDatabaseOperations()
    tables = ['auth_user', 'auth_group']
    sql_statements = db_ops.sql_flush(no_style(), tables, reset_sequences=False, allow_cascade=True)
    
    assert len(sql_statements) == 2
    assert "TRUNCATE TABLE auth_user" in sql_statements
    assert "TRUNCATE TABLE auth_group" in sql_statements