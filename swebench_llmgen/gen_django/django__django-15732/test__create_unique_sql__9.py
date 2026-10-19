import pytest
from django.contrib.auth.models import User
from django.db import connections
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

@pytest.fixture
def schema_editor():
    connection = connections['default']
    return BaseDatabaseSchemaEditor(connection=connection, collect_sql=False, atomic=True)

def test_create_unique_sql_without_constraints(schema_editor):
    model = User
    fields = [model._meta.get_field('username')]
    result = schema_editor._create_unique_sql(model, fields)

    assert result is not None
    assert result.sql == schema_editor.sql_create_unique
    assert result.name == schema_editor.quote_name("auth_user_username_uniq")

def test_create_unique_sql_with_condition(schema_editor):
    model = User
    fields = [model._meta.get_field('username')]
    condition = 'username IS NOT NULL'
    
    # Assume supports partial indexes is `True`
    schema_editor.connection.features.supports_partial_indexes = True
    result = schema_editor._create_unique_sql(model, fields, condition=condition)

    assert result is not None
    assert result.condition == schema_editor._index_condition_sql(condition)

def test_create_unique_sql_with_deferrable(schema_editor):
    model = User
    fields = [model._meta.get_field('username')]
    deferrable = Deferrable.DEFERRED
    
    schema_editor.connection.features.supports_deferrable_unique_constraints = True
    result = schema_editor._create_unique_sql(model, fields, deferrable=deferrable)

    assert result is not None
    assert result.deferrable == schema_editor._deferrable_constraint_sql(deferrable)

def test_create_unique_sql_with_include(schema_editor):
    model = User
    fields = [model._meta.get_field('username')]
    include = ['email']
    
    schema_editor.connection.features.supports_covering_indexes = True
    result = schema_editor._create_unique_sql(model, fields, include=include)

    assert result is not None
    assert result.include == schema_editor._index_include_sql(model, include)

def test_create_unique_sql_with_expressions(schema_editor):
    model = User
    fields = [model._meta.get_field('username')]
    expressions = ['LOWER(username)']
    
    schema_editor.connection.features.supports_expression_indexes = True
    result = schema_editor._create_unique_sql(model, fields, expressions=expressions)

    assert result is not None
    assert result.columns == schema_editor._index_columns(model._meta.db_table, expressions)

def test_create_unique_sql_with_unsupported_deferrable(schema_editor):
    model = User
    fields = [model._meta.get_field('username')]
    deferrable = Deferrable.DEFERRED
    
    schema_editor.connection.features.supports_deferrable_unique_constraints = False
    result = schema_editor._create_unique_sql(model, fields, deferrable=deferrable)

    assert result is None

def test_create_unique_sql_with_unsupported_partial_indexes(schema_editor):
    model = User
    fields = [model._meta.get_field('username')]
    condition = 'username IS NOT NULL'
    
    schema_editor.connection.features.supports_partial_indexes = False
    result = schema_editor._create_unique_sql(model, fields, condition=condition)

    assert result is None

def test_create_unique_sql_with_unsupported_covering_indexes(schema_editor):
    model = User
    fields = [model._meta.get_field('username')]
    include = ['email']
    
    schema_editor.connection.features.supports_covering_indexes = False
    result = schema_editor._create_unique_sql(model, fields, include=include)

    assert result is None

def test_create_unique_sql_with_unsupported_expression_indexes(schema_editor):
    model = User
    fields = [model._meta.get_field('username')]
    expressions = ['LOWER(username)']
    
    schema_editor.connection.features.supports_expression_indexes = False
    result = schema_editor._create_unique_sql(model, fields, expressions=expressions)

    assert result is None