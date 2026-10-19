import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

def test_create_unique_sql_with_no_constraints():
    editor = BaseDatabaseSchemaEditor(connection)
    sql_statement = editor._create_unique_sql(
        model=User,
        fields=[User._meta.get_field('username')],
    )
    
    assert sql_statement is not None
    assert sql_statement.sql == editor.sql_create_unique
    assert sql_statement.columns[0].name == 'username'


def test_create_unique_sql_with_deferrable_constraints():
    editor = BaseDatabaseSchemaEditor(connection)
    editor.connection.features.supports_deferrable_unique_constraints = True
    sql_statement = editor._create_unique_sql(
        model=User,
        fields=[User._meta.get_field('username')],
        deferrable=Deferrable.DEFERRED
    )
    
    assert sql_statement is not None
    assert sql_statement.deferrable == editor._deferrable_constraint_sql(Deferrable.DEFERRED)


def test_create_unique_sql_with_condition():
    editor = BaseDatabaseSchemaEditor(connection)
    editor.connection.features.supports_partial_indexes = True
    sql_statement = editor._create_unique_sql(
        model=User,
        fields=[User._meta.get_field('username')],
        condition="username IS NOT NULL"
    )
    
    assert sql_statement is not None
    assert sql_statement.condition == "username IS NOT NULL"
    assert sql_statement.sql == editor.sql_create_unique_index


def test_create_unique_sql_with_include():
    editor = BaseDatabaseSchemaEditor(connection)
    editor.connection.features.supports_covering_indexes = True
    sql_statement = editor._create_unique_sql(
        model=User,
        fields=[User._meta.get_field('username')],
        include=['email']
    )
    
    assert sql_statement is not None
    assert 'email' in sql_statement.include


def test_create_unique_sql_with_expressions():
    editor = BaseDatabaseSchemaEditor(connection)
    editor.connection.features.supports_expression_indexes = True
    sql_statement = editor._create_unique_sql(
        model=User,
        fields=[User._meta.get_field('username')],
        expressions=["LOWER(username)"]
    )
    
    assert sql_statement is not None
    assert sql_statement.columns[0].name == 'LOWER(username)'