import pytest
from django.db.models import Q
from django.core.exceptions import FieldError
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

@pytest.fixture
def query_instance():
    user_model = User
    return Query(model=user_model, alias_cols={})

def test_build_filter_valid_dict(query_instance):
    filter_expr = {'username': 'testuser'}
    clause, used_joins = query_instance.build_filter(filter_expr)
    assert clause is not None
    assert used_joins == []

def test_build_filter_valid_q_object(query_instance):
    filter_expr = Q(username='testuser')
    clause, used_joins = query_instance.build_filter(filter_expr)
    assert clause is not None
    assert used_joins == []

def test_build_filter_invalid_dict(query_instance):
    filter_expr = {}
    with pytest.raises(FieldError, match="Cannot parse keyword query"):
        query_instance.build_filter(filter_expr)

def test_build_filter_non_conditional_expression(query_instance):
    class NonConditionalExpression:
        conditional = False
        def resolve_expression(self, query, allow_joins=True):
            return None

    filter_expr = NonConditionalExpression()
    with pytest.raises(TypeError, match="Cannot filter against a non-conditional expression."):
        query_instance.build_filter(filter_expr)

def test_build_filter_empty_key(query_instance):
    filter_expr = ('', 'testuser')
    with pytest.raises(FieldError, match="Cannot parse keyword query"):
        query_instance.build_filter(filter_expr)

def test_build_filter_reuse_with_filtered_relation(query_instance):
    filter_expr = ('username', 'testuser')
    clause, used_joins = query_instance.build_filter(filter_expr, reuse_with_filtered_relation=True)
    assert clause is not None
    assert used_joins == []

def test_build_filter_joined_field_not_allowed(query_instance):
    filter_expr = ('profile__name', 'john')
    with pytest.raises(FieldError, match="Joined field references are not permitted in this query"):
        query_instance.build_filter(filter_expr, allow_joins=False)

def test_build_filter_invalid_lookup(query_instance):
    filter_expr = ('invalid_field', 'value')
    with pytest.raises(FieldError):
        query_instance.build_filter(filter_expr)

def test_build_filter_conditional_logic(query_instance):
    filter_expr = ('email', 'user@example.com')
    clause, used_joins = query_instance.build_filter(filter_expr)
    assert clause is not None
    assert 'email' in str(clause)

def test_build_filter_is_null_condition(query_instance):
    filter_expr = ('username', None)
    clause, used_joins = query_instance.build_filter(filter_expr)
    assert clause is not None
    assert 'IS NULL' in str(clause)