import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_set_values_with_fields():
    # Create a Query object using the User model
    query = Query(User, alias_cols=False)

    # Test setting values with specific fields
    fields = ['username', 'email']
    query.set_values(fields)

    assert query.values_select == ('username', 'email')
    assert query.select_related is False
    assert query.extra_select_mask == ()
    assert query.annotation_select_mask == ()

def test_set_values_with_extra_and_annotations():
    query = Query(User, alias_cols=False)
    query.extra_select = {'extra_field': 'extra'}
    query.annotation_select = {'annotated_field': 'annotated'}
    
    fields = ['username', 'extra_field', 'annotated_field']
    query.set_values(fields)

    assert query.values_select == ('username',)
    assert query.extra_select_mask == ('extra_field',)
    assert query.annotation_select_mask == ('annotated_field',)

def test_set_values_with_no_fields():
    query = Query(User, alias_cols=False)

    # Test setting values with no fields
    query.set_values([])

    expected_fields = [f.attname for f in User._meta.concrete_fields]
    assert query.values_select == tuple(expected_fields)

def test_set_values_with_group_by_true():
    query = Query(User, alias_cols=False)
    query.group_by = True

    fields = ['username']
    query.set_values(fields)

    assert query.values_select == ('username',)
    assert query.group_by is False  # Should disable GROUP BY aliases

def test_set_values_with_group_by_annotations():
    query = Query(User, alias_cols=False)
    query.group_by = ['annotated_field']
    query.annotation_select = {'annotated_field': 'annotated'}

    fields = ['username']
    query.set_values(fields)

    assert query.values_select == ('username',)
    assert query.group_by == ('annotated_field',)