import pytest
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_resolve_lookup_value_expression():
    # Arrange
    query = Query(model=User)
    expression = F('username')

    # Act
    resolved_value = query.resolve_lookup_value(expression, can_reuse=True, allow_joins=False, simple_col=True)

    # Assert
    assert resolved_value.contains_expression
    assert resolved_value.col == 'username'

def test_resolve_lookup_value_list_of_expressions():
    # Arrange
    query = Query(model=User)
    expressions = [F('username'), F('email')]

    # Act
    resolved_value = query.resolve_lookup_value(expressions, can_reuse=True, allow_joins=False, simple_col=True)

    # Assert
    assert isinstance(resolved_value, tuple)
    assert len(resolved_value) == 2
    assert resolved_value[0].contains_expression
    assert resolved_value[1].contains_expression

def test_resolve_lookup_value_tuple_of_expressions():
    # Arrange
    query = Query(model=User)
    expressions = (F('username'), F('first_name'))

    # Act
    resolved_value = query.resolve_lookup_value(expressions, can_reuse=True, allow_joins=False, simple_col=True)

    # Assert
    assert isinstance(resolved_value, tuple)
    assert len(resolved_value) == 2
    assert resolved_value[0].contains_expression
    assert resolved_value[1].contains_expression

def test_resolve_lookup_value_non_expression():
    # Arrange
    query = Query(model=User)
    value = 'sample_username'

    # Act
    resolved_value = query.resolve_lookup_value(value, can_reuse=True, allow_joins=False, simple_col=False)

    # Assert
    assert resolved_value == value

def test_resolve_lookup_value_mixed_values():
    # Arrange
    query = Query(model=User)
    mixed_values = [F('username'), 'sample_username']

    # Act
    resolved_value = query.resolve_lookup_value(mixed_values, can_reuse=True, allow_joins=False, simple_col=False)

    # Assert
    assert isinstance(resolved_value, tuple)
    assert len(resolved_value) == 2
    assert resolved_value[0].contains_expression
    assert resolved_value[1] == 'sample_username'