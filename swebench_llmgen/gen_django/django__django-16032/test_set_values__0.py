import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

@pytest.fixture
def user_query():
    user = User.objects.create_user('testuser', 'test@example.com', 'password')
    return Query(model=User, alias_cols=False)

def test_set_values_with_fields(user_query):
    user_query.set_values(['username', 'email'])
    
    assert user_query.values_select == ('username', 'email')
    assert not user_query.extra_select_mask
    assert not user_query.annotation_select_mask

def test_set_values_with_extra_fields(user_query):
    user_query.extra_select = {'extra_field': 'extra_value'}
    user_query.set_values(['username', 'extra_field'])
    
    assert user_query.values_select == ('username',)
    assert user_query.extra_select_mask == ('extra_field',)
    
def test_set_values_with_annotations(user_query):
    user_query.annotation_select = {'annotated_field': 'annotated_value'}
    user_query.set_values(['username', 'annotated_field'])
    
    assert user_query.values_select == ('username',)
    assert user_query.annotation_select_mask == ('annotated_field',)

def test_set_values_no_fields(user_query):
    user_query.set_values(None)

    expected_fields = [f.attname for f in User._meta.concrete_fields]
    assert set(user_query.values_select) == set(expected_fields)

def test_set_values_with_group_by(user_query):
    user_query.group_by = True
    user_query.set_values(['username', 'email'])

    assert user_query.values_select == ('username', 'email')
    assert user_query.group_by is False  # Should clear group by

def test_set_values_with_invalid_fields(user_query):
    user_query.extra_select = {'something_else': 'value'}
    user_query.set_values(['nonexistent_field'])

    assert user_query.values_select == ('nonexistent_field',)
    assert not user_query.extra_select_mask