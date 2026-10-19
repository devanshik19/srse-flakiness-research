import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.query import Query

def test_combine_queries_same_model():
    # Create two Query objects with the same model
    user_query_1 = Query(User)
    user_query_2 = Query(User)

    # Test valid combination with AND connector
    combined_query_and = user_query_1.combine(user_query_2, 'AND')
    assert combined_query_and.model == User

    # Test valid combination with OR connector
    combined_query_or = user_query_1.combine(user_query_2, 'OR')
    assert combined_query_or.model == User

def test_combine_queries_different_models():
    user_query = Query(User)
    # Create a fake query with a different model (to raise TypeError)
    class FakeModel:
        pass

    fake_query = Query(FakeModel)

    with pytest.raises(TypeError, match='Cannot combine queries on two different base models.'):
        user_query.combine(fake_query, 'AND')

def test_combine_queries_is_sliced():
    user_query = Query(User)
    user_query.is_sliced = True
    other_user_query = Query(User)

    with pytest.raises(TypeError, match='Cannot combine queries once a slice has been taken.'):
        user_query.combine(other_user_query, 'AND')

def test_combine_queries_different_distinct():
    user_query = Query(User)
    other_user_query = Query(User)
    user_query.distinct = True
    other_user_query.distinct = False

    with pytest.raises(TypeError, match='Cannot combine a unique query with a non-unique query.'):
        user_query.combine(other_user_query, 'AND')

def test_combine_queries_different_distinct_fields():
    user_query = Query(User)
    other_user_query = Query(User)
    user_query.distinct_fields = ['field1']
    other_user_query.distinct_fields = ['field2']

    with pytest.raises(TypeError, match='Cannot combine queries with different distinct fields.'):
        user_query.combine(other_user_query, 'AND')