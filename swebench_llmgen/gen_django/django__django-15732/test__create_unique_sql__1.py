import pytest
from django.contrib.auth.models import User
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

class MockConnection:
    class features:
        supports_deferrable_unique_constraints = True
        supports_partial_indexes = True
        supports_covering_indexes = True
        supports_expression_indexes = True

@pytest.fixture
def schema_editor():
    connection = MockConnection()
    return BaseDatabaseSchemaEditor(connection=connection, collect_sql=False, atomic=False)

def test_create_unique_sql_no_conditions(schema_editor):
    user_model = User
    fields = [user_model._meta.get_field('username')]
    result = schema_editor._create_unique_sql(user_model, fields)
    
    assert result is not None
    assert result.sql == schema_editor.sql_create_unique

def test_create_unique_sql_with_name(schema_editor):
    user_model = User
    fields = [user_model._meta.get_field('username')]
    unique_name = "unique_username"
    result = schema_editor._create_unique_sql(user_model, fields, name=unique_name)
    
    assert result is not None
    assert result.name == schema_editor.quote_name(unique_name)

def test_create_unique_sql_with_condition(schema_editor):
    user_model = User
    fields = [user_model._meta.get_field('username')]
    condition = "username IS NOT NULL"
    result = schema_editor._create_unique_sql(user_model, fields, condition=condition)
    
    assert result is not None
    assert result.sql == schema_editor.sql_create_unique_index

def test_create_unique_sql_with_deferrable(schema_editor):
    user_model = User
    fields = [user_model._meta.get_field('username')]
    result = schema_editor._create_unique_sql(user_model, fields, deferrable=Deferrable.INITIALLY_DEFERRED)
    
    assert result is not None
    assert result.deferrable == schema_editor._deferrable_constraint_sql(Deferrable.INITIALLY_DEFERRED)

def test_create_unique_sql_with_include(schema_editor):
    user_model = User
    fields = [user_model._meta.get_field('username')]
    include = ['email']
    result = schema_editor._create_unique_sql(user_model, fields, include=include)
    
    assert result is not None
    assert result.include == schema_editor._index_include_sql(user_model, include)

def test_create_unique_sql_with_expression(schema_editor):
    user_model = User
    fields = [user_model._meta.get_field('username')]
    expressions = ['LOWER(username)']
    result = schema_editor._create_unique_sql(user_model, fields, expressions=expressions)
    
    assert result is not None
    assert result.columns == schema_editor._index_columns(user_model._meta.db_table, expressions)

def test_create_unique_sql_conditions_not_supported(schema_editor):
    schema_editor.connection.features.supports_deferrable_unique_constraints = False
    user_model = User
    fields = [user_model._meta.get_field('username')]
    
    result = schema_editor._create_unique_sql(user_model, fields, deferrable=Deferrable.INITIALLY_DEFERRED)
    
    assert result is None