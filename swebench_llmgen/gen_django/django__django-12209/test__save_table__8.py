import pytest
from django.contrib.auth.models import User
from django.db import DatabaseError

@pytest.fixture
def user_instance():
    return User(username='testuser', password='password')

def test_save_table_insert(user_instance):
    """Test saving a new instance of User."""
    assert user_instance.pk is None  # No primary key initially
    user_instance.save()
    assert user_instance.pk is not None  # Primary key should be set after saving

def test_save_table_update(user_instance):
    """Test updating an existing instance of User."""
    user_instance.save()
    original_pk = user_instance.pk
    user_instance.username = 'updateduser'
    user_instance._save_table(using='default', cls=User)
    
    # Reload the instance to check if it was updated
    user_instance.refresh_from_db()
    assert user_instance.username == 'updateduser'
    assert user_instance.pk == original_pk

def test_save_table_force_update(user_instance):
    """Test forced update of an existing instance of User."""
    user_instance.save()
    original_username = user_instance.username
    user_instance.username = 'updateduser'
    
    # Attempt to force update
    user_instance._save_table(force_update=True, using='default', cls=User, update_fields=['username'])
    
    # Reload the instance to check if it was updated
    user_instance.refresh_from_db()
    assert user_instance.username == 'updateduser'
    
def test_save_table_force_update_no_pk(user_instance):
    """Test that trying a forced update without a primary key raises an error."""
    user_instance.pk = None  # Reset primary key to simulate no pk situation
    with pytest.raises(ValueError, match="Cannot force an update in save\\(\\) with no primary key."):
        user_instance._save_table(force_update=True, using='default', cls=User)

def test_save_table_update_not_found(user_instance):
    """Test that update with update_fields raises an error when no rows were affected."""
    user_instance.save()
    user_instance.username = 'newusername'
    user_instance._save_table(using='default', cls=User, update_fields=['username'])
    
    # Assume it points to something that's nonexistent; should raise DatabaseError
    with pytest.raises(DatabaseError, match="Save with update_fields did not affect any rows."):
        user_instance._save_table(force_update=True, using='default', cls=User, update_fields=['username'])