import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

@pytest.fixture
def schema_editor():
    return BaseDatabaseSchemaEditor(connection)

def test_delete_composed_index_valid(schema_editor):
    # Create a User model instance
    user = User(username='testuser', password='password')
    user.save()
    
    # Create a composed index on the User model
    schema_editor.execute('CREATE INDEX test_user_idx ON auth_user (username, password);')
    
    # Attempt to delete the composed index
    sql = "DROP INDEX test_user_idx;"
    schema_editor._delete_composed_index(User, ['username', 'password'], {}, sql)
    
    # Check if the index is actually deleted
    with pytest.raises(Exception):
        schema_editor.execute('SELECT * FROM auth_user WHERE username = %s AND password = %s;', ['testuser', 'password'])

def test_delete_composed_index_invalid_count(schema_editor):
    # Create a User model instance
    user = User(username='testuser', password='password')
    user.save()
    
    # Create a single index on the User model (not composed)
    schema_editor.execute('CREATE INDEX test_user_single_idx ON auth_user (username);')
    
    # Attempt to delete the composed index (should raise ValueError)
    sql = "DROP INDEX test_user_single_idx;"
    with pytest.raises(ValueError, match="Found wrong number"):
        schema_editor._delete_composed_index(User, ['username', 'password'], {}, sql)

def test_delete_composed_index_no_constraints(schema_editor):
    # Create a User model instance
    user = User(username='testuser', password='password')
    user.save()
    
    # Attempt to delete without any index or constraints
    sql = "DROP INDEX nonexistent_index;"
    with pytest.raises(ValueError, match="Found wrong number"):
        schema_editor._delete_composed_index(User, ['username', 'password'], {}, sql)