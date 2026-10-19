import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

@pytest.fixture
def schema_editor():
    return BaseDatabaseSchemaEditor(connection=connection, collect_sql=False, atomic=True)

def test_create_unique_sql_without_conditions(schema_editor):
    user_model = User
    fields = [user_model._meta.get_field('username')]
    
    # Testing without any optional parameters
    sql_statement = schema_editor._create_unique_sql(model=user_model, fields=fields)
    
    assert sql_statement is not None
    assert sql_statement.sql == schema_editor.sql_create_unique

def test_create_unique_sql_with_name(schema_editor):
    user_model = User
    fields = [user_model._meta.get_field('username')]
    name = "custom_unique_name"
    
    sql_statement = schema_editor._create_unique_sql(model=user_model, fields=fields, name=name)
    
    assert sql_statement is not None
    assert sql_statement.name == schema_editor.quote_name(name)

def test_create_unique_sql_with_condition(schema_editor):
    user_model = User
    fields = [user_model._meta.get_field('username')]
    condition = "username IS NOT NULL"

    sql_statement = schema_editor._create_unique_sql(model=user_model, fields=fields, condition=condition)
    
    assert sql_statement is not None
    assert sql_statement.sql == schema_editor.sql_create_unique_index

def test_create_unique_sql_with_deferrable(schema_editor):
    user_model = User
    fields = [user_model._meta.get_field('username')]
    deferrable = Deferrable.DEFERRED

    sql_statement = schema_editor._create_unique_sql(model=user_model, fields=fields, deferrable=deferrable)
    
    assert sql_statement is not None

def test_create_unique_sql_when_deferrable_not_supported(schema_editor):
    user_model = User
    fields = [user_model._meta.get_field('username')]
    schema_editor.connection.features.supports_deferrable_unique_constraints = False

    sql_statement = schema_editor._create_unique_sql(model=user_model, fields=fields, deferrable=True)
    
    assert sql_statement is None

def test_create_unique_sql_with_include(schema_editor):
    user_model = User
    fields = [user_model._meta.get_field('username')]
    include = ['email']

    sql_statement = schema_editor._create_unique_sql(model=user_model, fields=fields, include=include)
    
    assert sql_statement is not None
    assert sql_statement.sql == schema_editor.sql_create_unique_index

def test_create_unique_sql_with_expressions(schema_editor):
    user_model = User
    fields = [user_model._meta.get_field('username')]
    expressions = ['LOWER(username)']

    sql_statement = schema_editor._create_unique_sql(model=user_model, fields=fields, expressions=expressions)
    
    assert sql_statement is not None
    assert sql_statement.sql == schema_editor.sql_create_unique_index

def test_create_unique_sql_with_all_conditions(schema_editor):
    user_model = User
    fields = [user_model._meta.get_field('username')]
    condition = "username IS NOT NULL"
    deferrable = Deferrable.DEFERRED
    include = ['email']
    expressions = ['LOWER(username)']

    sql_statement = schema_editor._create_unique_sql(model=user_model, fields=fields, condition=condition, deferrable=deferrable, include=include, expressions=expressions)
    
    assert sql_statement is not None
    assert sql_statement.sql == schema_editor.sql_create_unique_index