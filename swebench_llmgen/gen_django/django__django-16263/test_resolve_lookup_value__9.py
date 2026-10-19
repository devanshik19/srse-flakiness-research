import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_resolve_lookup_value_with_expression():
    query = Query(User)
    class DummyExpression:
        def resolve_expression(self, query, reuse, allow_joins):
            return 'resolved_expression'

    result = query.resolve_lookup_value(DummyExpression(), can_reuse=False, allow_joins=False)
    assert result == 'resolved_expression'

def test_resolve_lookup_value_with_list():
    query = Query(User)
    result = query.resolve_lookup_value([1, 2, 3], can_reuse=False, allow_joins=False)
    assert result == [1, 2, 3]

def test_resolve_lookup_value_with_tuple():
    query = Query(User)
    result = query.resolve_lookup_value((4, 5), can_reuse=False, allow_joins=False)
    assert result == (4, 5)

def test_resolve_lookup_value_with_namedtuple():
    from collections import namedtuple
    Point = namedtuple('Point', ['x', 'y'])
    point = Point(10, 20)
    query = Query(User)
    result = query.resolve_lookup_value(point, can_reuse=False, allow_joins=False)
    assert result == Point(10, 20)

def test_resolve_lookup_value_without_expression():
    query = Query(User)
    result = query.resolve_lookup_value(42, can_reuse=False, allow_joins=False)
    assert result == 42