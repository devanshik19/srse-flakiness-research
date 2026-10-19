import pytest
from django.contrib.auth.models import User
from django.core.exceptions import DatabaseError

@pytest.mark.django_db
def test_save_table_insert():
    user = User(username='testuser', password='testpass')
    assert user._save_table(cls=User, force_insert=True) is True
    user.save()
    assert user.pk is not None

@pytest.mark.django_db
def test_save_table_update():
    user = User.objects.create(username='testuser', password='testpass')
    user.username = 'updateduser'
    updated = user._save_table(cls=User)
    assert updated is True
    user.save()
    assert User.objects.get(pk=user.pk).username == 'updateduser'

@pytest.mark.django_db
def test_save_table_update_force_update():
    user = User.objects.create(username='testuser', password='testpass')
    user.username = 'updateduser'
    updated = user._save_table(cls=User, force_update=True)
    assert updated is True
    user.save()
    assert User.objects.get(pk=user.pk).username == 'updateduser'

@pytest.mark.django_db
def test_save_table_no_pk_force_update():
    user = User(username='testuser', password='testpass')
    with pytest.raises(ValueError, match="Cannot force an update in save() with no primary key."):
        user._save_table(cls=User, force_update=True)

@pytest.mark.django_db
def test_save_table_with_update_fields():
    user = User(username='testuser', password='testpass')
    user.save()
    user._save_table(update_fields=['username'], cls=User)
    assert User.objects.get(pk=user.pk).username == 'testuser'

@pytest.mark.django_db
def test_save_table_no_update_fields():
    user = User(username='testuser', password='testpass')
    user.save()
    user._save_table(cls=User)
    assert User.objects.get(pk=user.pk).username == 'testuser'