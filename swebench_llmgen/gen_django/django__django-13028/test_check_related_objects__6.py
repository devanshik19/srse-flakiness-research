import pytest
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.db.models.sql.query import Query


def test_check_related_objects_with_query_set():
    user1 = User.objects.create(username='testuser1')
    user2 = User.objects.create(username='testuser2')
    
    query = Query(model=User)
    
    # This should not raise an exception
    query.check_related_objects(User._meta.get_field('username'), User.objects.filter(username='testuser1'), User._meta)

    with pytest.raises(ValueError):
        query.check_related_objects(User._meta.get_field('username'), User.objects.all(), User._meta)


def test_check_related_objects_with_instance():
    user = User.objects.create(username='checkuser')

    query = Query(model=User)
    
    # This should not raise an exception because we're passing a valid instance
    query.check_related_objects(User._meta.get_field('username'), user, User._meta)


def test_check_related_objects_with_iterable():
    user1 = User.objects.create(username='iteruser1')
    user2 = User.objects.create(username='iteruser2')

    users = [user1, user2]
    
    query = Query(model=User)
    
    # This should not raise an exception
    query.check_related_objects(User._meta.get_field('username'), users, User._meta)


def test_check_related_objects_with_invalid_instance():
    class FakeModel:
        _meta = type('Meta', (), {'object_name': 'FakeModel'})

    fake_instance = FakeModel()
    query = Query(model=User)
    
    with pytest.raises(ValueError):
        query.check_related_objects(User._meta.get_field('username'), fake_instance, User._meta)