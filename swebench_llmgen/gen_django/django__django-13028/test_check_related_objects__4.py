import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_check_related_objects_valid_queryset():
    query = Query(model=User)
    author_field = User._meta.get_field('username')  # This is usually a valid field
    valid_queryset = User.objects.all()
    
    # Should not raise an error
    query.check_related_objects(author_field, valid_queryset, User._meta)


def test_check_related_objects_invalid_queryset():
    query = Query(model=User)
    author_field = User._meta.get_field('username')
    other_model_queryset = User.objects.filter(is_active=False)  # QuerySet for another condition
    
    with pytest.raises(ValueError) as excinfo:
        query.check_related_objects(author_field, other_model_queryset, User._meta)
    
    assert 'Cannot use QuerySet for' in str(excinfo.value)


def test_check_related_objects_iterable():
    query = Query(model=User)
    author_field = User._meta.get_field('username')
    valid_user_list = [User(username='user1'), User(username='user2')]
    
    # Should not raise an error for valid iterable
    query.check_related_objects(author_field, valid_user_list, User._meta)


def test_check_related_objects_invalid_iterable():
    query = Query(model=User)
    author_field = User._meta.get_field('username')
    invalid_user_list = ['not_a_user', 'not_a_user2']
    
    with pytest.raises(ValueError) as excinfo:
        query.check_related_objects(author_field, invalid_user_list, User._meta)
    
    assert 'Cannot use QuerySet for' in str(excinfo.value)