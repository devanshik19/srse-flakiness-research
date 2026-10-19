import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query
from django.core.exceptions import ValueError

def test_check_related_objects_with_queryset():
    user_queryset = User.objects.all()
    query_instance = Query(model=User, where=None, alias_cols=None)

    with pytest.raises(ValueError) as excinfo:
        query_instance.check_related_objects(User._meta.get_field('username'), user_queryset, User._meta)
    
    assert str(excinfo.value) == 'Cannot use QuerySet for "User": Use a QuerySet for "User".'

def test_check_related_objects_with_correct_model_instance():
    user_instance = User(username='testuser')
    query_instance = Query(model=User, where=None, alias_cols=None)

    try:
        query_instance.check_related_objects(User._meta.get_field('username'), user_instance, User._meta)
    except ValueError:
        pytest.fail("ValueError raised unexpectedly!")

def test_check_related_objects_with_iterable():
    user_instances = [User(username='user1'), User(username='user2')]
    query_instance = Query(model=User, where=None, alias_cols=None)

    try:
        query_instance.check_related_objects(User._meta.get_field('username'), user_instances, User._meta)
    except ValueError:
        pytest.fail("ValueError raised unexpectedly!")

def test_check_related_objects_with_invalid_object_type():
    invalid_instance = "Invalid String"
    query_instance = Query(model=User, where=None, alias_cols=None)

    with pytest.raises(ValueError):
        query_instance.check_related_objects(User._meta.get_field('username'), invalid_instance, User._meta)