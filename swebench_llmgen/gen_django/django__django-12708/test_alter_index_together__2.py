import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

@pytest.fixture
def schema_editor():
    return BaseDatabaseSchemaEditor(connection)

def test_alter_index_together_create(schema_editor):
    # Setup: Create a test user and index together
    User._meta.indexes.clear()  # Clear existing indexes
    old_index_together = [['username', 'email']]
    new_index_together = [['username'], ['email']]
    
    # Act: Call the method to alter index together
    schema_editor.alter_index_together(User, old_index_together, new_index_together)
    
    # Assert: Check that new indexes are created
    user_indexes = User._meta.indexes
    assert len(user_indexes) == 2
    assert any(index.fields == ['username'] for index in user_indexes)
    assert any(index.fields == ['email'] for index in user_indexes)

def test_alter_index_together_delete(schema_editor):
    # Setup: Create a test user and index together
    User._meta.indexes.clear()  # Clear existing indexes
    old_index_together = [['username'], ['email']]
    new_index_together = [['username', 'email']]
    
    # Act: Call the method to alter index together
    schema_editor.alter_index_together(User, old_index_together, new_index_together)
    
    # Assert: Check that the old indexes have been deleted, new one is created
    user_indexes = User._meta.indexes
    assert len(user_indexes) == 1
    assert user_indexes[0].fields == ['username', 'email']