import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

@pytest.fixture
def query():
    user_model = User
    return Query(model=user_model, alias_cols={})

def test_set_values_with_fields(query):
    fields = ['username', 'email']
    query.set_values(fields)
    
    assert query.values_select == ('username', 'email')
    assert query.select_related is False

def test_set_values_with_extra_and_annotations(query):
    query.extra_select = {'extra_field': 'Count(*)'}
    query.annotation_select = {'annotated_field': 'Count(username)'}
    
    fields = ['username', 'extra_field', 'annotated_field']
    query.set_values(fields)
    
    assert query.values_select == ('username', 'extra_field', 'annotated_field')
    assert query.select_related is False

def test_set_values_empty_fields(query):
    query.set_values([])
    
    expected_fields = [f.attname for f in query.model._meta.concrete_fields]
    assert sorted(query.values_select) == sorted(expected_fields)
    assert query.select_related is False

def test_set_values_with_group_by_true(query):
    query.group_by = True
    fields = ['username', 'email']
    query.set_values(fields)
    
    assert query.values_select == ('username', 'email')
    assert len(query.group_by) == len(query.model._meta.concrete_fields)

def test_set_values_with_group_by_fields(query):
    query.group_by = ['username']
    fields = ['username', 'email']
    query.set_values(fields)
    
    assert query.values_select == ('username', 'email')
    assert len(query.group_by) == 1
    assert query.group_by[0].refs == 'username'