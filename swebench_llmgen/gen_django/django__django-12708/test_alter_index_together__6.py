import pytest
from django.contrib.auth.models import User
from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

@pytest.fixture
def db_schema_editor():
    connection.set_schema_editor(BaseDatabaseSchemaEditor)
    return connection.schema_editor()

def test_alter_index_together_create_index(db_schema_editor):
    user = User.objects.create(username='testuser')
    old_index_together = [['username']]
    new_index_together = [['username'], ['email']]

    # Initially create the index together
    db_schema_editor.alter_index_together(User, old_index_together, new_index_together)

    # Verify that the new index has been created
    assert 'idx_user_email' in db_schema_editor.connection.introspection.get_indexes(User._meta.db_table)
    assert 'idx_user_username' in db_schema_editor.connection.introspection.get_indexes(User._meta.db_table)

def test_alter_index_together_remove_index(db_schema_editor):
    user1 = User.objects.create(username='testuser1', email='user1@example.com')
    user2 = User.objects.create(username='testuser2', email='user2@example.com')

    old_index_together = [['username'], ['email']]
    new_index_together = [['username']]

    # Initially create the index together
    db_schema_editor.alter_index_together(User, old_index_together, new_index_together)

    # Check that the email index was removed
    assert 'idx_user_email' not in db_schema_editor.connection.introspection.get_indexes(User._meta.db_table)

def test_alter_index_together_no_change(db_schema_editor):
    user = User.objects.create(username='testuser')
    old_index_together = [['username']]
    new_index_together = [['username']]

    # No changes to indexes
    db_schema_editor.alter_index_together(User, old_index_together, new_index_together)

    # Verify that no new indexes were created or removed
    indexes = db_schema_editor.connection.introspection.get_indexes(User._meta.db_table)
    assert len(indexes) == 1  # Should only have one index for username
    assert 'idx_user_username' in indexes

def test_alter_index_together_multiple_indexes(db_schema_editor):
    user1 = User.objects.create(username='testuser1', email='user1@example.com')
    user2 = User.objects.create(username='testuser2', email='user2@example.com')

    old_index_together = [['username'], ['email']]
    new_index_together = [['username'], ['email'], ['first_name']]

    # Test adding new index
    db_schema_editor.alter_index_together(User, old_index_together, new_index_together)

    # Verify that the new index on first_name is created
    assert 'idx_user_first_name' in db_schema_editor.connection.introspection.get_indexes(User._meta.db_table)