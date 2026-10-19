import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

@pytest.fixture
def schema_editor():
    return BaseDatabaseSchemaEditor(connection)

def test_delete_composed_index_success(schema_editor):
    # Prepare a test user model instance
    user = User(username='testuser', password='password123')
    user.save()

    # Create an index on 'username'
    with connection.schema_editor() as editor:
        editor.execute("CREATE INDEX idx_username ON auth_user (username);")
        assert connection.introspection.get_constraints('auth_user')['idx_username']

    # Delete the composed index
    sql = "DELETE INDEX idx_username;"
    schema_editor._delete_composed_index(User, ['username'], {}, sql)

    # Verify that the index no longer exists
    assert 'idx_username' not in connection.introspection.get_constraints('auth_user')

def test_delete_composed_index_wrong_number_of_constraints(schema_editor):
    # Prepare a test user model instance
    user = User(username='testuser', password='password123')
    user.save()

    # Test for duplicate index name
    sql = "DELETE INDEX idx_nonexistent;"
    
    with pytest.raises(ValueError, match="Found wrong number"):
        schema_editor._delete_composed_index(User, ['username'], {}, sql)