import pytest
from django.contrib.auth.models import User
from django.db import DatabaseError

def test_save_table_insert():
    user = User(username='testuser', password='testpass')
    assert user._state.adding is True
    user.save()
    assert user.pk is not None

def test_save_table_update():
    user = User.objects.create(username='testuser', password='testpass')
    user.username = 'updateduser'
    user.save()
    updated_user = User.objects.get(pk=user.pk)
    assert updated_user.username == 'updateduser'

def test_save_table_force_update():
    user = User.objects.create(username='testuser', password='testpass')
    user.username = 'forceupdateuser'
    user.save(force_update=True)
    updated_user = User.objects.get(pk=user.pk)
    assert updated_user.username == 'forceupdateuser'

def test_save_table_with_update_fields():
    user = User.objects.create(username='testuser', password='testpass')
    user.username = 'updatefielduser'
    user.save(update_fields=['username'])
    updated_user = User.objects.get(pk=user.pk)
    assert updated_user.username == 'updatefielduser'

def test_save_table_no_primary_key():
    user = User(username='testuser', password='testpass')
    with pytest.raises(ValueError, match="Cannot force an update in save() with no primary key."):
        user.save(force_update=True)

def test_save_table_update_without_effect():
    user = User(username='testuser', password='testpass')
    user.save()
    user.username = 'sameusername'
    with pytest.raises(DatabaseError, match="Save with update_fields did not affect any rows."):
        user.save(update_fields=['username'])

def test_save_table_ordering_field():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    assert user1._order == 0
    assert user2._order == 1