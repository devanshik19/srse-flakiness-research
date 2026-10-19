import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.query import Query

@pytest.fixture
def user_query():
    return User.objects.all()

@pytest.fixture
def another_user_query():
    return User.objects.filter(is_active=True)

def test_combine_same_model(user_query, another_user_query):
    combined_query = user_query.combine(another_user_query.query, Q.AND)

    assert combined_query.model == User
    assert combined_query.where == user_query.query.where
    assert combined_query.extra == user_query.query.extra
    assert combined_query.order_by == user_query.query.order_by

def test_combine_different_models(user_query):
    with pytest.raises(TypeError) as excinfo:
        combined_query = user_query.combine(User.objects.filter(is_staff=True).query, Q.AND)
    assert str(excinfo.value) == 'Cannot combine queries on two different base models.'

def test_combine_on_sliced_query(user_query):
    sliced_query = user_query[:10]
    with pytest.raises(TypeError) as excinfo:
        combined_query = sliced_query.combine(another_user_query.query, Q.AND)
    assert str(excinfo.value) == 'Cannot combine queries once a slice has been taken.'

def test_combine_different_distinct(user_query, another_user_query):
    user_query.distinct = True
    another_user_query.distinct = False
    with pytest.raises(TypeError) as excinfo:
        combined_query = user_query.combine(another_user_query.query, Q.AND)
    assert str(excinfo.value) == 'Cannot combine a unique query with a non-unique query.'

def test_combine_different_distinct_fields(user_query, another_user_query):
    user_query.distinct_fields = ['email']
    another_user_query.distinct_fields = ['username']
    with pytest.raises(TypeError) as excinfo:
        combined_query = user_query.combine(another_user_query.query, Q.AND)
    assert str(excinfo.value) == 'Cannot combine queries with different distinct fields.'

def test_combine_and_reuse_joins(user_query, another_user_query):
    user_query.distinct_fields = []
    combined_query = user_query.combine(another_user_query.query, Q.AND)

    assert combined_query.alias_map is not None
    assert len(combined_query.alias_map) >= len(user_query.query.alias_map)

def test_combine_or_with_extra(user_query, another_user_query):
    user_query.extra['select'] = ['COUNT(*) AS user_count']
    another_user_query.extra['select'] = ['COUNT(*) AS active_user_count']

    with pytest.raises(ValueError) as excinfo:
        combined_query = user_query.combine(another_user_query.query, Q.OR)
    assert str(excinfo.value) == "When merging querysets using 'or', you cannot have extra(select=...) on both sides."