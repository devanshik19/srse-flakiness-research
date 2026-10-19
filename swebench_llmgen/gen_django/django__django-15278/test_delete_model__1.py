import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.sqlite3.schema import DatabaseSchemaEditor

@pytest.fixture
def schema_editor():
    editor = DatabaseSchemaEditor(connection)
    yield editor
    editor.execute("DROP TABLE IF EXISTS auth_user;")

def test_delete_model_with_handle_autom2m(schema_editor):
    # Arrange
    user = User(username='testuser')
    user.save()
    assert User.objects.count() == 1
    
    # Act
    schema_editor.delete_model(User)

    # Assert
    assert User.objects.count() == 0

def test_delete_model_without_handle_autom2m(schema_editor):
    # Arrange
    user = User(username='testuser')
    user.save()
    assert User.objects.count() == 1
    
    # Act
    schema_editor.delete_model(User, handle_autom2m=False)

    # Assert
    assert User.objects.count() == 0