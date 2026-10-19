import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

@pytest.fixture
def schema_editor():
    return BaseDatabaseSchemaEditor(connection)

def test_create_unique_sql_no_constraint(schema_editor):
    result = schema_editor._create_unique_sql(User, ['username'])
    assert result is not None
    assert result.table.table == 'auth_user'
    assert 'username' in result.columns

def test_create_unique_sql_with_deferrable(schema_editor):
    schema_editor.connection.features.supports_deferrable_unique_constraints = True
    result = schema_editor._create_unique_sql(User, ['username'], deferrable='deferred')
    assert result is not None
    assert 'username' in result.columns

def test_create_unique_sql_with_condition(schema_editor):
    schema_editor.connection.features.supports_partial_indexes = True
    result = schema_editor._create_unique_sql(User, ['username'], condition='is_active = True')
    assert result is not None
    assert 'username' in result.columns

def test_create_unique_sql_with_include(schema_editor):
    schema_editor.connection.features.supports_covering_indexes = True
    result = schema_editor._create_unique_sql(User, ['username'], include=['email'])
    assert result is not None
    assert 'username' in result.columns
    assert 'email' in result.include

def test_create_unique_sql_with_expression(schema_editor):
    schema_editor.connection.features.supports_expression_indexes = True
    result = schema_editor._create_unique_sql(User, [], expressions=['LOWER(username)'])
    assert result is not None
    assert isinstance(result.columns, list)

def test_create_unique_sql_deferrable_not_supported(schema_editor):
    schema_editor.connection.features.supports_deferrable_unique_constraints = False
    result = schema_editor._create_unique_sql(User, ['username'], deferrable='deferred')
    assert result is None

def test_create_unique_sql_condition_not_supported(schema_editor):
    schema_editor.connection.features.supports_partial_indexes = False
    result = schema_editor._create_unique_sql(User, ['username'], condition='is_active = True')
    assert result is None

def test_create_unique_sql_include_not_supported(schema_editor):
    schema_editor.connection.features.supports_covering_indexes = False
    result = schema_editor._create_unique_sql(User, ['username'], include=['email'])
    assert result is None

def test_create_unique_sql_expressions_not_supported(schema_editor):
    schema_editor.connection.features.supports_expression_indexes = False
    result = schema_editor._create_unique_sql(User, [], expressions=['LOWER(username)'])
    assert result is None