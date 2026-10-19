import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

@pytest.fixture
def query():
    # Create a Query object for the User model
    user_model = User
    return Query(user_model)

def test_set_values_with_fields(query):
    # Test with specific field names
    fields = ['username', 'email']
    query.set_values(fields)
    assert query.values_select == ('username', 'email')
    assert query.select_related is False

def test_set_values_with_extra(query):
    # Setup extra select fields
    query.extra_select = {'extra_field': 'Some value'}
    fields = ['username', 'extra_field']
    query.set_values(fields)
    assert query.values_select == ('username',)
    assert query.extra_select_mask == ('extra_field',)

def test_set_values_with_annotations(query):
    # Setup annotation select fields
    query.annotation_select = {'annotated_field': 'Some value'}
    fields = ['username', 'annotated_field']
    query.set_values(fields)
    assert query.values_select == ('username',)
    assert query.annotation_select_mask == ('annotated_field',)

def test_set_values_no_fields(query):
    # Test with no fields provided
    query.set_values([])
    assert query.values_select == tuple(f.attname for f in query.model._meta.concrete_fields)

def test_set_values_group_by(query):
    # Test with group_by set to True
    query.group_by = True
    fields = ['username']
    query.set_values(fields)
    assert query.values_select == ('username',)
    assert query.group_by is False

def test_set_values_group_by_with_annotations(query):
    # Test with existing group_by and annotations
    query.annotation_select = {'annotated_field': 'Some value'}
    query.group_by = [query.get_meta().get_field('username')]
    fields = ['username']
    query.set_values(fields)
    assert query.group_by == (query.get_meta().get_field('username'),)