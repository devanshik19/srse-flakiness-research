import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.sqlite3.schema import DatabaseSchemaEditor

@pytest.mark.django_db
def test_delete_model_handle_autom2m():
    # Arrange
    user = User.objects.create(username='testuser')
    db_editor = DatabaseSchemaEditor(connection)
    
    # Act
    db_editor.delete_model(User)

    # Assert
    with pytest.raises(User.DoesNotExist):
        User.objects.get(username='testuser')

@pytest.mark.django_db
def test_delete_model_no_handle_autom2m():
    # Arrange
    user = User.objects.create(username='testuser')
    db_editor = DatabaseSchemaEditor(connection)
    
    # Act
    db_editor.delete_model(User, handle_autom2m=False)

    # Assert
    with pytest.raises(User.DoesNotExist):
        User.objects.get(username='testuser')

    # Ensure that deferred SQL related to the model is cleared.
    assert len(db_editor.deferred_sql) == 0