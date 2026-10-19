import pytest
from django.db.models import Q
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_combine_same_model():
    # Create two Query instances based on the same model
    query1 = User.objects.all().query
    query2 = User.objects.filter(is_staff=True).query

    # Combine queries with AND
    combined_query_and = query1.combine(query2, Q.AND)
    assert combined_query_and == query1.filter(is_staff=True)

    # Combine queries with OR
    combined_query_or = query1.combine(query2, Q.OR)
    assert combined_query_or == query1.filter(Q(is_staff=True) | Q(id__isnull=False))

def test_combine_different_models():
    # Create two Query instances based on different models
    query1 = User.objects.all().query
    query2 = User.objects.filter(is_active=True).query

    with pytest.raises(TypeError, match='Cannot combine queries on two different base models.'):
        query1.combine(query2, Q.AND)

def test_combine_sliced_query():
    # Create a sliced query
    query1 = User.objects.all()[:5].query
    query2 = User.objects.filter(is_staff=True).query

    with pytest.raises(TypeError, match='Cannot combine queries once a slice has been taken.'):
        query1.combine(query2, Q.AND)

def test_combine_distinct_queries():
    # Create two queries with different distinct settings
    query1 = User.objects.distinct().query
    query2 = User.objects.filter(is_staff=True).distinct().query

    with pytest.raises(TypeError, match='Cannot combine queries with different distinct fields.'):
        query1.combine(query2, Q.AND)