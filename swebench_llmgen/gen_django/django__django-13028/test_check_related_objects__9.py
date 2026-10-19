import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query
from django.core.exceptions import ValueError

def test_check_related_objects_with_valid_queryset():
    user_query = User.objects.all()  # A valid queryset
    q = Query(model=User, where=None, alias_cols=None)
    q.check_related_objects(User._meta.get_field('username'), user_query, User._meta)

def test_check_related_objects_with_invalid_queryset():
    user_query = User.objects.all()
    q = Query(model=User, where=None, alias_cols=None)

    with pytest.raises(ValueError) as excinfo:
        q.check_related_objects(User._meta.get_field('username'), user_query, User._meta)
    assert 'Use a QuerySet for' in str(excinfo.value)

def test_check_related_objects_with_single_object():
    user = User(username='test_user')
    q = Query(model=User, where=None, alias_cols=None)
    
    q.check_related_objects(User._meta.get_field('username'), user, User._meta)

def test_check_related_objects_with_iterable():
    users = [User(username='user1'), User(username='user2')]
    q = Query(model=User, where=None, alias_cols=None)
    
    q.check_related_objects(User._meta.get_field('username'), users, User._meta)

def test_check_related_objects_with_invalid_type():
    q = Query(model=User, where=None, alias_cols=None)
    
    with pytest.raises(ValueError):
        q.check_related_objects(User._meta.get_field('username'), 123, User._meta)