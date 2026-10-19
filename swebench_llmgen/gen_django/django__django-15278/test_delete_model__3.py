import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.sqlite3.schema import DatabaseSchemaEditor

@pytest.fixture
def schema_editor():
    return DatabaseSchemaEditor(connection)

def test_delete_model_deletes_table_and_deferred_sql(schema_editor):
    user_model = User
    # Create user and use schema editor to create the table
    schema_editor.create_model(user_model)

    # Ensure the table exists
    assert connection.introspection.table_names() == [user_model._meta.db_table]

    # Add a deferred SQL statement for the User model
    deferred_sql_statement = f"CREATE INDEX index_user_on_username ON {user_model._meta.db_table} (username)"
    schema_editor.deferred_sql.append(Statement(deferred_sql_statement))

    # Check that the deferred statement is added
    assert len(schema_editor.deferred_sql) == 1

    # Delete the User model
    schema_editor.delete_model(user_model, handle_autom2m=False)

    # Ensure the table has been deleted
    assert user_model._meta.db_table not in connection.introspection.table_names()

    # Ensure deferred SQL referencing the deleted table has been removed
    assert len(schema_editor.deferred_sql) == 0

def test_delete_model_with_handle_autom2m(schema_editor):
    user_model = User
    # Create user and use schema editor to create the table
    schema_editor.create_model(user_model)

    # Ensure the table exists
    assert connection.introspection.table_names() == [user_model._meta.db_table]

    # Delete the User model with handle_autom2m=True
    schema_editor.delete_model(user_model, handle_autom2m=True)

    # Ensure the table has been deleted
    assert user_model._meta.db_table not in connection.introspection.table_names()