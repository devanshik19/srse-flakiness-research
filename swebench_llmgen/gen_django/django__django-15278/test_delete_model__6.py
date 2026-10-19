import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

@pytest.mark.usefixtures("django_db_setup")
def test_delete_model_handle_autom2m():
    user = User.objects.create(username='testuser')
    editor = BaseDatabaseSchemaEditor(connection)
    
    # Test deletion with handle_autom2m=True
    editor.delete_model(User)
    
    with pytest.raises(User.DoesNotExist):
        User.objects.get(username='testuser')

def test_delete_model_without_handle_autom2m():
    user = User.objects.create(username='testuser')
    editor = BaseDatabaseSchemaEditor(connection)
    
    # Test deletion with handle_autom2m=False
    editor.delete_model(User, handle_autom2m=False)
    
    with pytest.raises(User.DoesNotExist):
        User.objects.get(username='testuser')

    # To verify if the deferred_sql entries are cleared
    assert len(editor.deferred_sql) == 0