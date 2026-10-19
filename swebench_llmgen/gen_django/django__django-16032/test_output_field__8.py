import pytest
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.db.models.sql.query import Query

@pytest.fixture
def setup_query():
    # Create a query on the User model
    return Query(User, alias_cols={}, default_cols='*', select=[])

def test_output_field_single_select(setup_query):
    query = setup_query
    # Simulate a single select field
    query.select = [User._meta.get_field('username')]
    assert query.output_field() == User._meta.get_field('username')

def test_output_field_single_annotation_select(setup_query):
    query = setup_query
    # Simulate a single annotation
    query.annotation_select = {'annotated_field': Count('id')}
    assert query.output_field() == query.annotation_select['annotated_field'].output_field

def test_output_field_multiple_selects(setup_query):
    query = setup_query
    # Simulate multiple selects
    query.select = [User._meta.get_field('username'), User._meta.get_field('email')]
    assert query.output_field() is None  # Should not return a field if multiple selects are present

def test_output_field_no_selects(setup_query):
    query = setup_query
    # Simulate no selects
    query.select = []
    query.annotation_select = {}
    assert query.output_field() is None  # Should return None if no select or annotation is present