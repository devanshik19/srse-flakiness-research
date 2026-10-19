import pytest
from django.contrib.auth.models import User
from django.db import DatabaseError

@pytest.mark.django_db
def test_save_table_insert():
    # Test inserting a new User instance
    user = User(username='testuser', email='testuser@example.com', password='password')
    user._save_table(force_insert=True, cls=User)
    assert user.pk is not None

@pytest.mark.django_db
def test_save_table_update():
    # Test updating an existing User instance
    user = User.objects.create(username='testuser', email='testuser@example.com', password='password')
    user.email = 'updated@example.com'
    updated = user._save_table(cls=User)
    assert updated is True
    assert User.objects.get(pk=user.pk).email == 'updated@example.com'

@pytest.mark.django_db
def test_save_table_update_fields():
    # Test updating specific fields
    user = User.objects.create(username='testuser', email='testuser@example.com', password='password')
    user.email = 'updated@example.com'
    updated = user._save_table(update_fields=['email'], cls=User)
    assert updated is True
    assert User.objects.get(pk=user.pk).email == 'updated@example.com'

@pytest.mark.django_db
def test_save_table_no_primary_key_update():
    # Test forcing an update without a primary key should raise an error
    user = User(username='testuser', email='testuser@example.com', password='password')
    # Not saving so user.pk is None
    with pytest.raises(ValueError):
        user._save_table(force_update=True, cls=User)

@pytest.mark.django_db
def test_save_table_force_update_no_change():
    # Test that forcing an update without any changes raises DatabaseError
    user = User.objects.create(username='testuser', email='testuser@example.com', password='password')
    with pytest.raises(DatabaseError):
        user._save_table(force_update=True, cls=User, update_fields=[])

@pytest.mark.django_db
def test_save_table_order_with_respect_to():
    # Test order_with_respect_to functionality
    user1 = User.objects.create(username='testuser1', email='testuser1@example.com', password='password')
    user2 = User.objects.create(username='testuser2', email='testuser2@example.com', password='password')
    user1._state.order_with_respect_to = user2
    updated = user1._save_table(cls=User)
    assert updated is True
    assert user1._order is not None