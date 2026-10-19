import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.sqlite3.schema import DatabaseSchemaEditor

@pytest.mark.django_db
def test_delete_model_handle_autom2m():
    # Create a user instance
    user = User.objects.create_user(username='testuser', password='password')

    # Get the schema editor
    schema_editor = DatabaseSchemaEditor(connection)

    # Verify the table exists before deletion
    assert User._meta.db_table in connection.introspection.table_names()

    # Delete the model with handle_autom2m = True
    schema_editor.delete_model(User, handle_autom2m=True)

    # Check that the table has been deleted
    assert User._meta.db_table not in connection.introspection.table_names()

@pytest.mark.django_db
def test_delete_model_no_handle_autom2m():
    # Create a user instance
    user = User.objects.create_user(username='testuser', password='password')

    # Get the schema editor
    schema_editor = DatabaseSchemaEditor(connection)

    # Verify the table exists before deletion
    assert User._meta.db_table in connection.introspection.table_names()

    # Delete the model with handle_autom2m = False
    schema_editor.delete_model(User, handle_autom2m=False)

    # Check that the table has been deleted
    assert User._meta.db_table not in connection.introspection.table_names()