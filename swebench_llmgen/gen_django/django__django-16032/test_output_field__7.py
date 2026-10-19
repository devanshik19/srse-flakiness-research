import pytest
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.db.models.sql.query import Query

@pytest.fixture
def user_query():
    # Create a QuerySet for User model to work with
    return User.objects.all()

def test_output_field_single_select(user_query):
    # Create a Query instance with a single select field from the User model
    query = Query(User, [])
    query.select = [query._get_col('id', User._meta.get_field('id'), 'id')]
    result = query.output_field()
    assert result == User._meta.get_field('id')

def test_output_field_single_annotation(user_query):
    # Create a Query instance with a single annotation field
    query = Query(User, [])
    query.annotation_select = {
        'annotated_count': Count('id')
    }
    query.annotation_select['annotated_count'].output_field = User._meta.get_field('id')
    result = query.output_field()
    assert result == User._meta.get_field('id')

def test_output_field_multiple_selects(user_query):
    # Create a Query instance with multiple select fields
    query = Query(User, [])
    query.select = [
        query._get_col('username', User._meta.get_field('username'), 'username'),
        query._get_col('email', User._meta.get_field('email'), 'email')
    ]
    result = query.output_field()
    assert result is None  # Should return None when there are multiple selects

def test_output_field_multiple_annotations(user_query):
    # Create a Query instance with multiple annotations
    query = Query(User, [])
    query.annotation_select = {
        'annotated_count': Count('id'),
        'annotated_username': User._meta.get_field('username')
    }
    result = query.output_field()
    assert result is None  # Should return None when there are multiple annotations