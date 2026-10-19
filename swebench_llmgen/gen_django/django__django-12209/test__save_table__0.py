import pytest
from django.contrib.auth.models import User
from django.db import DatabaseError

def test_save_table_insert():
    user = User(username='testuser', email='test@example.com')
    user.save()

    assert user.pk is not None  # Ensure the user was saved and has a primary key

def test_save_table_update():
    user = User.objects.create(username='testuser', email='test@example.com')
    original_email = user.email
    user.email = 'newemail@example.com'
    user._save_table(force_update=True, cls=User)

    user.refresh_from_db()
    assert user.email == 'newemail@example.com'
    assert user.email != original_email

def test_save_table_update_no_pk():
    user = User(username='testuser')
    with pytest.raises(ValueError, match="Cannot force an update in save() with no primary key."):
        user._save_table(force_update=True, cls=User)

def test_save_table_insert_with_default_pk():
    user = User(username='testuser')
    user._state.adding = True  # Simulate an instance that is new and should be inserted
    user._save_table(cls=User)

    assert user.pk is not None

def test_save_table_update_fields():
    user = User.objects.create(username='testuser', email='test@example.com')
    user.email = 'updated@example.com'
    user._save_table(update_fields=['email'], cls=User)

    user.refresh_from_db()
    assert user.email == 'updated@example.com'

def test_save_table_force_insert():
    user = User(username='testuser', email='test@example.com')
    user.save()

    original_pk = user.pk
    user.email = 'newemail@example.com'
    
    user._save_table(force_insert=True, cls=User)

    assert user.pk != original_pk  # Check that a new instance was created
    assert user.email == 'newemail@example.com'

def test_save_table_update_fields_no_update():
    user = User.objects.create(username='testuser', email='test@example.com')
    user.email = 'email@example.com'
    
    user._save_table(update_fields=['nonexistent_field'], cls=User)

    user.refresh_from_db()
    assert user.email == 'test@example.com'  # No changes should be applied

def test_save_table_force_update_no_rows():
    user = User.objects.create(username='testuser', email='test@example.com')
    
    with pytest.raises(DatabaseError, match="Forced update did not affect any rows."):
        user._save_table(force_update=True, cls=User)