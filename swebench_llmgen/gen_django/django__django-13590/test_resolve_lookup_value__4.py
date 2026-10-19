import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_resolve_lookup_value_single_expression():
    query = Query(model=User)
    expression = User.objects.all()  # Assume this is the expression
    resolved_value = query.resolve_lookup_value(expression, can_reuse=True, allow_joins=True)

    assert resolved_value is not None  # Check that the value is resolved

def test_resolve_lookup_value_with_list():
    query = Query(model=User)
    expressions = [User(username='testuser1'), User(username='testuser2')]
    resolved_values = query.resolve_lookup_value(expressions, can_reuse=True, allow_joins=True)

    assert isinstance(resolved_values, list)  # Ensure it returns a list
    assert len(resolved_values) == len(expressions)  # Check count is correct
    # Check each value in the resolved list is not None
    for value in resolved_values:
        assert value is not None

def test_resolve_lookup_value_with_tuple():
    query = Query(model=User)
    expressions = (User(username='testuser1'), User(username='testuser2'))
    resolved_values = query.resolve_lookup_value(expressions, can_reuse=True, allow_joins=True)

    assert isinstance(resolved_values, tuple)  # Ensure it returns a tuple
    assert len(resolved_values) == len(expressions)  # Check count is correct
    # Check each value in the resolved tuple is not None
    for value in resolved_values:
        assert value is not None

def test_resolve_lookup_value_with_no_expression():
    query = Query(model=User)
    resolved_value = query.resolve_lookup_value('no_expression', can_reuse=True, allow_joins=True)

    assert resolved_value == 'no_expression'  # Check that the value is unchanged