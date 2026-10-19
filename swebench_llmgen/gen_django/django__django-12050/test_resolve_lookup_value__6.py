import pytest
from django.db.models.expressions import F
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

@pytest.fixture
def query():
    user_model = User._meta.model
    return Query(model=user_model, where=None)

def test_resolve_lookup_value_single_expression(query):
    expr = F('username')
    result = query.resolve_lookup_value(expr, can_reuse=True, allow_joins=False, simple_col=False)
    assert isinstance(result, F)
    assert result.name == 'username'

def test_resolve_lookup_value_list_of_expressions(query):
    expr_list = [F('username'), F('email')]
    result = query.resolve_lookup_value(expr_list, can_reuse=True, allow_joins=False, simple_col=False)
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], F)
    assert isinstance(result[1], F)
    assert result[0].name == 'username'
    assert result[1].name == 'email'

def test_resolve_lookup_value_mixed_expressions(query):
    expr_mixed = [F('username'), 'plain_value', F('email')]
    result = query.resolve_lookup_value(expr_mixed, can_reuse=True, allow_joins=False, simple_col=False)
    assert isinstance(result, tuple)
    assert len(result) == 3
    assert isinstance(result[0], F)
    assert result[0].name == 'username'
    assert result[1] == 'plain_value'
    assert isinstance(result[2], F)
    assert result[2].name == 'email'

def test_resolve_lookup_value_non_expression(query):
    result = query.resolve_lookup_value('just_a_string', can_reuse=True, allow_joins=False, simple_col=False)
    assert result == 'just_a_string'