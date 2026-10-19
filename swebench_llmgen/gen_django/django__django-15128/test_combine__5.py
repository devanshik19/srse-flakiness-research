import pytest
from django.db.models import Q
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_combine_same_model():
    q1 = Query(User)
    q2 = Query(User)

    # Assume both queries have no filters initially
    combined_query = q1.combine(q2, Q())  # Using AND connector
    assert combined_query == q1  # No changes should happen

def test_combine_different_models():
    q1 = Query(User)
    q2 = Query(User)  # This should represent another model, but using User for simplicity

    with pytest.raises(TypeError, match='Cannot combine queries on two different base models.'):
        q1.combine(q2, Q())

def test_combine_with_sliced_query():
    q1 = Query(User)
    q2 = Query(User)

    # Assume q1 has already been sliced
    q1.is_sliced = True

    with pytest.raises(TypeError, match='Cannot combine queries once a slice has been taken.'):
        q1.combine(q2, Q())

def test_combine_with_different_distinct():
    q1 = Query(User)
    q2 = Query(User)

    q1.distinct = True
    q2.distinct = False

    with pytest.raises(TypeError, match='Cannot combine a unique query with a non-unique query.'):
        q1.combine(q2, Q())

def test_combine_with_different_distinct_fields():
    q1 = Query(User)
    q2 = Query(User)

    q1.distinct_fields = ['username']
    q2.distinct_fields = ['email']

    with pytest.raises(TypeError, match='Cannot combine queries with different distinct fields.'):
        q1.combine(q2, Q())

def test_combine_with_and_connector():
    q1 = Query(User)
    q2 = Query(User)
    
    assert q1.combine(q2, Q()).where == q1.where
    
    # Manually add a filter to q2 for combining
    q2.where.add(Q(username='testuser'), Q())
    combined_query = q1.combine(q2, Q())
    
    assert len(combined_query.where.children) == 1
    assert 'testuser' in str(combined_query.where)

def test_combine_with_or_connector():
    q1 = Query(User)
    q2 = Query(User)

    # Let's define filters for both queries
    q1.where.add(Q(is_staff=True), Q())
    q2.where.add(Q(is_superuser=True), Q())
    
    combined_query = q1.combine(q2, Q())
    
    assert len(combined_query.where.children) == 2  # both conditions should exist
    assert q1.where in combined_query.where.children
    assert q2.where in combined_query.where.children

def test_combine_with_extra():
    q1 = Query(User)
    q2 = Query(User)

    q1.extra = {'select': ['field1']}
    q2.extra = {'select': ['field2']}

    combined_query = q1.combine(q2, Q())
    
    assert combined_query.extra == {'select': ['field1', 'field2']}