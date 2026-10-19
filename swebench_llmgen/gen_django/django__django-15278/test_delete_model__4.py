import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.sqlite3.schema import DatabaseSchemaEditor

@pytest.fixture
def schema_editor():
    return DatabaseSchemaEditor(connection)

def test_delete_model_with_autom2m(schema_editor):
    # Create a user model instance
    user = User.objects.create(username='testuser')
    
    # Check if user exists before deletion
    assert User.objects.filter(id=user.id).exists()
    
    # Delete model with handle_autom2m = True
    schema_editor.delete_model(User, handle_autom2m=True)

    # Verify that the User model is deleted
    assert not User.objects.filter(id=user.id).exists()

def test_delete_model_without_autom2m(schema_editor):
    # Create a user model instance
    user = User.objects.create(username='testuser')
    
    # Check if user exists before deletion
    assert User.objects.filter(id=user.id).exists()
    
    # Delete model with handle_autom2m = False
    schema_editor.delete_model(User, handle_autom2m=False)

    # Verify that the User model is deleted
    assert not User.objects.filter(id=user.id).exists()

def test_delete_model_updates_deferred_sql(schema_editor):
    # Create a user model instance
    user = User.objects.create(username='testuser')

    # Check the deferred_sql initially should be empty
    assert len(schema_editor.deferred_sql) == 0

    # Perform the delete model operation
    schema_editor.delete_model(User, handle_autom2m=False)

    # Check that deferred_sql is also updated after the table deletion
    assert all(not sql.references_table(User._meta.db_table) for sql in schema_editor.deferred_sql)