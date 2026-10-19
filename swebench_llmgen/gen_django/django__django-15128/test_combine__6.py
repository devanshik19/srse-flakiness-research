import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.query import Query

def test_combine_queries_same_model():
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')

    query1 = Query(User)
    query2 = Query(User)

    query1 = query1.filter(Q(username='user1'))
    query2 = query2.filter(Q(username='user2'))

    combined_query = query1.combine(query2, 'AND')
    results = list(combined_query)

    assert len(results) == 0  # No user should match both conditions

    combined_query_or = query1.combine(query2, 'OR')
    results_or = list(combined_query_or)

    assert len(results_or) == 2  # Both users should match the OR condition

def test_combine_queries_different_models():
    user_query = Query(User)
    group_query = Query(User).filter(Q(id=1))  # using User for simulation

    with pytest.raises(TypeError, match='Cannot combine queries on two different base models.'):
        user_query.combine(group_query, 'AND')

def test_combine_queries_sliced():
    query = Query(User).filter(Q(username='user1'))[:1]
    another_query = Query(User).filter(Q(username='user2'))

    with pytest.raises(TypeError, match='Cannot combine queries once a slice has been taken.'):
        query.combine(another_query, 'AND')

def test_combine_queries_different_distinct():
    user_query = Query(User).distinct()
    group_query = Query(User).distinct(fields=['username'])

    with pytest.raises(TypeError, match='Cannot combine queries with different distinct fields.'):
        user_query.combine(group_query, 'AND')

def test_combine_extra_queries():
    user_query = Query(User)
    user_query.extra['select'] = {'extra_field': 'username'}
    
    another_query = Query(User)
    another_query.extra['select'] = {'extra_field_2': 'first_name'}

    combined_query = user_query.combine(another_query, 'AND')
    assert 'extra_field' in combined_query.extra['select']
    assert 'extra_field_2' in combined_query.extra['select']