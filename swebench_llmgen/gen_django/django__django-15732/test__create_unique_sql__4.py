import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

@pytest.fixture
def schema_editor():
    return BaseDatabaseSchemaEditor(connection)

def test_create_unique_sql_without_name(schema_editor):
    user_model = User
    fields = [user_model._meta.get_field('username'), user_model._meta.get_field('email')]
    
    sql_statement = schema_editor._create_unique_sql(
        model=user_model,
        fields=fields
    )
    
    assert sql_statement is not None
    assert sql_statement.table.name == 'auth_user'
    assert 'CONSTRAINT' in sql_statement.sql

def test_create_unique_sql_with_name(schema_editor):
    user_model = User
    fields = [user_model._meta.get_field('username')]
    custom_name = 'custom_unique_username'

    sql_statement = schema_editor._create_unique_sql(
        model=user_model,
        fields=fields,
        name=custom_name
    )
    
    assert sql_statement.name == custom_name

def test_create_unique_sql_with_conditions(schema_editor):
    user_model = User
    fields = [user_model._meta.get_field('username')]
    condition = 'username IS NOT NULL'

    sql_statement = schema_editor._create_unique_sql(
        model=user_model,
        fields=fields,
        condition=condition
    )
    
    assert sql_statement is not None
    assert 'CONSTRAINT' in sql_statement.sql
    assert condition in sql_statement.condition

def test_create_unique_sql_with_deferrable(schema_editor):
    user_model = User
    fields = [user_model._meta.get_field('email')]
    deferrable = True

    sql_statement = schema_editor._create_unique_sql(
        model=user_model,
        fields=fields,
        deferrable=deferrable
    )
    
    assert sql_statement is not None
    assert 'DEFERRABLE' in sql_statement.deferrable

def test_create_unique_sql_with_include(schema_editor):
    user_model = User
    fields = [user_model._meta.get_field('username')]
    include = ['email']

    sql_statement = schema_editor._create_unique_sql(
        model=user_model,
        fields=fields,
        include=include
    )

    assert sql_statement is not None
    assert 'INCLUDE' in sql_statement.include

def test_create_unique_sql_with_expression(schema_editor):
    user_model = User
    fields = [user_model._meta.get_field('username')]
    expressions = ['LOWER(username)']

    sql_statement = schema_editor._create_unique_sql(
        model=user_model,
        fields=fields,
        expressions=expressions
    )

    assert sql_statement is not None
    assert 'EXCLUDE' in sql_statement.columns

def test_create_unique_sql_with_feature_support(schema_editor):
    user_model = User
    fields = [user_model._meta.get_field('username')]
    
    # Simulating a case where features are not supported
    schema_editor.connection.features.supports_deferrable_unique_constraints = False
    schema_editor.connection.features.supports_partial_indexes = False
    schema_editor.connection.features.supports_covering_indexes = False
    schema_editor.connection.features.supports_expression_indexes = False

    sql_statement = schema_editor._create_unique_sql(
        model=user_model,
        fields=fields,
        deferrable=True,
        condition='username IS NOT NULL',
        include=['email'],
        expressions=['LOWER(username)']
    )

    assert sql_statement is None