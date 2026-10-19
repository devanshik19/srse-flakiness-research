import pytest
from django.contrib.auth.models import User
from django.db import DatabaseError

@pytest.mark.django_db
def test_save_table_insert():
    user = User(username='testuser', password='password123')
    user.save()  # This should invoke _save_table and perform an INSERT
    assert user.pk is not None  # Ensure the user has been saved and has a primary key


@pytest.mark.django_db
def test_save_table_update():
    user = User.objects.create(username='testuser', password='password123')
    user.username = 'updateduser'
    updated = user.save(force_update=True)  # Should update the record
    assert updated == False  # No insert, update should return False
    user.refresh_from_db()
    assert user.username == 'updateduser'


@pytest.mark.django_db
def test_save_table_force_update_noprimarykey():
    user = User(username='testuser', password='password123')
    with pytest.raises(ValueError, match="Cannot force an update in save() with no primary key."):
        user.save(force_update=True)  # Should raise ValueError


@pytest.mark.django_db
def test_save_table_with_update_fields():
    user = User.objects.create(username='testuser', password='password123')
    user.password = 'newpassword123'
    updated = user.save(update_fields=['password'])  # Should update only the password
    assert updated == False  # No insert, update should return False
    user.refresh_from_db()
    assert user.password == 'newpassword123'


@pytest.mark.django_db
def test_save_table_insert_with_default_pk():
    user = User(username='testuser', password='password123')
    user.save()
    assert user.pk is not None  # The user should still be saved with a new primary key


@pytest.mark.django_db
def test_save_table_no_primary_key_with_force_insert():
    user = User(username='testuser2', password='password123')
    with pytest.raises(DatabaseError, match="Forced update did not affect any rows."):
        user.save(force_insert=True, force_update=True)  # Should raise DatabaseError