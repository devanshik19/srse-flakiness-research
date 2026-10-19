import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

@pytest.fixture
def user_query():
    return Query(model=User, alias_cols=[])

def test_set_values_with_field_names(user_query):
    user_query.set_values(['username', 'email'])
    assert user_query.values_select == ('username', 'email')
    assert user_query.select_related is False

def test_set_values_with_extra_and_annotation(user_query):
    user_query.extra_select = {'extra_field': 'value'}
    user_query.annotation_select = {'annotated_field': 'value'}
    
    user_query.set_values(['username', 'extra_field', 'annotated_field'])
    assert user_query.values_select == ('username',)
    assert user_query.extra_select_mask == {'extra_field'}
    assert user_query.annotation_select_mask == {'annotated_field'}

def test_set_values_with_empty_fields(user_query):
    user_query.set_values([])
    expected_fields = [f.attname for f in User._meta.concrete_fields]
    assert user_query.values_select == tuple(expected_fields)

def test_set_values_with_group_by_true(user_query):
    user_query.group_by = True
    user_query.set_values(['username'])
    assert user_query.group_by is False
    assert user_query.values_select == ('username',)
    
def test_set_values_with_group_by(user_query):
    user_query.group_by = ['annotated_field']
    user_query.annotation_select = {'annotated_field': 'value'}
    
    user_query.set_values(['username'])
    assert user_query.group_by == (user_query.annotation_select['annotated_field'],)
    assert user_query.values_select == ('username',)

def test_set_values_with_nonexistent_fields(user_query):
    user_query.extra_select = {'field1': 'value'}
    user_query.annotation_select = {'field2': 'value'}
    
    user_query.set_values(['field3'])
    assert user_query.values_select == ('field3',)
    assert user_query.extra_select_mask == set()
    assert user_query.annotation_select_mask == set()