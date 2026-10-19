import pytest
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.db.models.sql.query import Query
from django.core.exceptions import ValueError

def test_check_related_objects_with_valid_queryset():
    query = Query(User, None, None)
    user_queryset = User.objects.all()

    # Should not raise an error for valid QuerySet
    query.check_related_objects(User._meta.get_field('username'), user_queryset, User._meta)

def test_check_related_objects_with_invalid_queryset():
    query = Query(User, None, None)
    group_queryset = User.objects.values('groups')  # Invalid QuerySet for User

    with pytest.raises(ValueError) as excinfo:
        query.check_related_objects(User._meta.get_field('username'), group_queryset, User._meta)
    
    assert str(excinfo.value) == 'Cannot use QuerySet for "Group": Use a QuerySet for "User".'

def test_check_related_objects_with_single_object():
    query = Query(User, None, None)
    user_instance = User(username='testuser')
    
    # Should not raise an error for valid User instance
    query.check_related_objects(User._meta.get_field('username'), user_instance, User._meta)

def test_check_related_objects_with_iterable_of_objects():
    query = Query(User, None, None)
    user_instances = [User(username='testuser1'), User(username='testuser2')]

    # Should not raise an error for valid User instances iterable
    query.check_related_objects(User._meta.get_field('username'), user_instances, User._meta)

def test_check_related_objects_with_invalid_iterable():
    query = Query(User, None, None)
    mixed_instances = [User(username='testuser'), object()]

    with pytest.raises(ValueError) as excinfo:
        query.check_related_objects(User._meta.get_field('username'), mixed_instances, User._meta)
    
    assert str(excinfo.value).startswith('Cannot use QuerySet for')