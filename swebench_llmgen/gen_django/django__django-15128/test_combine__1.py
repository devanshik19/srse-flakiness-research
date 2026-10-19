import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.query import Query


@pytest.fixture
def user_query():
    query_a = Query(User)
    query_b = Query(User)
    return query_a, query_b


def test_combine_different_models(user_query):
    query_a, query_b = user_query
    query_b.model = 'DifferentModel'  # Simulating different model

    with pytest.raises(TypeError, match='Cannot combine queries on two different base models.'):
        query_a.combine(query_b, 'AND')


def test_combine_sliced_query(user_query):
    query_a, query_b = user_query
    query_a.is_sliced = True  # Simulating a sliced query

    with pytest.raises(TypeError, match='Cannot combine queries once a slice has been taken.'):
        query_a.combine(query_b, 'AND')


def test_combine_different_distinct(user_query):
    query_a, query_b = user_query
    query_a.distinct = True
    query_b.distinct = False

    with pytest.raises(TypeError, match='Cannot combine a unique query with a non-unique query.'):
        query_a.combine(query_b, 'AND')


def test_combine_different_distinct_fields(user_query):
    query_a, query_b = user_query
    query_a.distinct_fields = ('field1',)
    query_b.distinct_fields = ('field2',)

    with pytest.raises(TypeError, match='Cannot combine queries with different distinct fields.'):
        query_a.combine(query_b, 'AND')


def test_combine_and_connector(user_query):
    query_a, query_b = user_query
    query_b.alias_map = {'alias1': None}  # Setup some dummy alias map
    query_a.join_class = query_b.join_class  # Use same join class for both

    combined_query = query_a.combine(query_b, 'AND')

    assert combined_query is not None
    # Here you can add further assertions on `combined_query` properties if needed


def test_combine_or_connector(user_query):
    query_a, query_b = user_query
    query_b.alias_map = {'alias1': None}

    combined_query = query_a.combine(query_b, 'OR')

    assert combined_query is not None
    # Assert expected properties on the combined query