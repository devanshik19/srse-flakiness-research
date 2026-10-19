import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

@pytest.fixture
def schema_editor():
    return BaseDatabaseSchemaEditor(connection)

def test_alter_index_together_create_index(schema_editor):
    # Set up initial index_together settings
    old_index_together = [['username']]
    new_index_together = [['username', 'email']]
    
    # Create a test model
    User._meta.indexes = []
    
    # Call the method to alter index together
    schema_editor.alter_index_together(User, old_index_together, new_index_together)

    # Check if the new index is created
    assert len(User._meta.indexes) == 1
    assert str(User._meta.indexes[0]) == 'Index(fields=[username, email], name=index_user_username_email)'

def test_alter_index_together_remove_index(schema_editor):
    # Set up initial index_together settings with an existing index
    old_index_together = [['username', 'email']]
    new_index_together = [['username']]
    
    # Create an index
    User._meta.indexes = [Index(fields=['username', 'email'], name='index_user_username_email')]

    # Call the method to alter index together
    schema_editor.alter_index_together(User, old_index_together, new_index_together)

    # Check if the previous index is removed
    assert len(User._meta.indexes) == 0