import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.query import Query
from django.core.exceptions import FieldError, TypeError

@pytest.fixture
def user_query():
    return Query(User, alias_cols=None)

def test_build_filter_with_valid_dict(user_query):
    filter_expr = {'username': 'testuser'}
    clause, used_joins = user_query.build_filter(filter_expr)
    assert clause is not None
    assert isinstance(clause, WhereNode)

def test_build_filter_with_q_object(user_query):
    filter_expr = Q(username='testuser')
    clause, used_joins = user_query.build_filter(filter_expr)
    assert clause is not None
    assert isinstance(clause, WhereNode)

def test_build_filter_with_non_conditional_expression(user_query):
    class NonConditionalExpression:
        def resolve_expression(self, query, allow_joins=True):
            return self

    filter_expr = NonConditionalExpression()
    with pytest.raises(TypeError, match="Cannot filter against a non-conditional expression."):
        user_query.build_filter(filter_expr)

def test_build_filter_with_empty_key(user_query):
    filter_expr = ("", "testuser")
    with pytest.raises(FieldError, match="Cannot parse keyword query"):
        user_query.build_filter(filter_expr)

def test_build_filter_with_invalid_dict(user_query):
    filter_expr = {}
    with pytest.raises(FieldError, match="Cannot parse keyword query as dict"):
        user_query.build_filter(filter_expr)

def test_build_filter_with_reffed_expression(user_query):
    filter_expr = ('username', 'testuser')
    clause, used_joins = user_query.build_filter(filter_expr, allow_joins=True)
    assert clause is not None
    assert isinstance(clause, WhereNode)

def test_build_filter_with_join_restriction(user_query):
    filter_expr = ('profile__bio', 'test bio')
    with pytest.raises(FieldError, match="Joined field references are not permitted in this query"):
        user_query.build_filter(filter_expr, allow_joins=False)

def test_build_filter_handling_nullable(user_query):
    filter_expr = ('is_active', True)
    clause, used_joins = user_query.build_filter(filter_expr, current_negated=True)
    assert clause is not None
    assert isinstance(clause, WhereNode)

def test_build_filter_with_multi_join_exception(user_query):
    filter_expr = ('email', 'nonexistent@example.com')
    with pytest.raises(MultiJoin):
        user_query.build_filter(filter_expr)