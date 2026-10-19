import pytest
from django.contrib.auth.models import User
from django.db.models import Q, FieldError
from django.db.models.sql.query import Query

@pytest.fixture
def user_query():
    return Query(model=User)

def test_build_filter_valid_dict(user_query):
    filter_expr = {'username': 'testuser'}
    clause, used_joins = user_query.build_filter(filter_expr)
    assert clause is not None
    assert len(used_joins) == 0

def test_build_filter_valid_q_object(user_query):
    filter_expr = Q(username='testuser')
    clause, used_joins = user_query.build_filter(filter_expr)
    assert clause is not None
    assert len(used_joins) == 0

def test_build_filter_invalid_dict(user_query):
    filter_expr = {}
    with pytest.raises(FieldError):
        user_query.build_filter(filter_expr)

def test_build_filter_non_conditional_expression(user_query):
    class NonConditional:
        conditional = False
        
        def resolve_expression(self, query, allow_joins=True):
            return self
    
    filter_expr = NonConditional()
    with pytest.raises(TypeError):
        user_query.build_filter(filter_expr)

def test_build_filter_invalid_arg(user_query):
    filter_expr = (None, 'value')
    with pytest.raises(FieldError):
        user_query.build_filter(filter_expr)

def test_build_filter_with_negation(user_query):
    filter_expr = ('username', 'testuser')
    clause, used_joins = user_query.build_filter(filter_expr, current_negated=True)
    assert clause is not None
    assert len(used_joins) == 0