import pytest
from django.contrib.auth.models import User
from django.db import DatabaseError

@pytest.mark.django_db
def test_save_table_insert():
    user = User(username='testuser', password='testpass')
    user.save()
    assert user.pk is not None

@pytest.mark.django_db
def test_save_table_update():
    user = User.objects.create(username='testuser', password='testpass')
    user.username = 'updateduser'
    user.save()
    updated_user = User.objects.get(pk=user.pk)
    assert updated_user.username == 'updateduser'

@pytest.mark.django_db
def test_save_table_force_update_without_pk():
    user = User(username='testuser', password='testpass')
    user.save()
    user.username = 'forcedupdate'
    
    with pytest.raises(ValueError):
        user.save(force_update=True)

@pytest.mark.django_db
def test_save_table_force_insert():
    user = User(username='testuser', password='testpass')
    user.save()
    user.pk = None  # Reset primary key to simulate a new instance
    user.username = 'newuser'
    user.save(force_insert=True)
    assert User.objects.filter(username='newuser').exists()

@pytest.mark.django_db
def test_save_table_update_fields():
    user = User.objects.create(username='testuser', password='testpass')
    user.username = 'updateduser'
    user.save(update_fields=['username'])
    
    updated_user = User.objects.get(pk=user.pk)
    assert updated_user.username == 'updateduser'

@pytest.mark.django_db
def test_save_table_update_fields_no_effect():
    user = User.objects.create(username='testuser', password='testpass')
    user.username = 'updateduser'
    user.save(update_fields=['username'])
    
    user.username = 'anotheruser'
    user.save(update_fields=['nonexistent_field'])  # No update should happen
    
    updated_user = User.objects.get(pk=user.pk)
    assert updated_user.username == 'updateduser'