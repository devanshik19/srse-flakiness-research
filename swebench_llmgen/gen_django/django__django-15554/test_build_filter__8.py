import pytest
from django.db.models import Q
from django.db.models.sql.query import Query
from django.contrib.auth.models import User
from django.core.exceptions import FieldError, TypeError


def test_build_filter_with_dict_raises_field_error():
    query = Query()
    with pytest.raises(FieldError, match="Cannot parse keyword query as dict"):
        query.build_filter({'username': 'testuser'})


def test_build_filter_with_q_object():
    query = Query()
    filter_expr = Q(username='testuser')
    where_node, used_joins = query.build_filter(filter_expr)
    assert isinstance(where_node, WhereNode)
    assert len(used_joins) == 0  # No joins should be used


def test_build_filter_with_condition_expression():
    query = Query()
    user = User(username='testuser', email='test@example.com')
    user.save()
    
    # this should work without errors and produce a WhereNode
    condition_expression = query.resolve_expression(F('username'))
    where_node, used_joins = query.build_filter(('username', 'testuser'))
    assert isinstance(where_node, WhereNode)
    assert len(used_joins) == 0


def test_build_filter_with_invalid_lookup_type_raises_field_error():
    query = Query()
    with pytest.raises(FieldError, match="Cannot parse keyword query None"):
        query.build_filter((None, 'value'))


def test_build_filter_with_non_conditional_expression_raises_type_error():
    query = Query()
    class NonConditionalExpression:
        conditional = False

        def resolve_expression(self, query, allow_joins=True):
            return self

    non_conditional_expr = NonConditionalExpression()
    
    with pytest.raises(TypeError, match="Cannot filter against a non-conditional expression."):
        query.build_filter(non_conditional_expr)


def test_build_filter_with_multiple_lookups_on_relation_raises_field_error():
    query = Query()
    user = User(username='testuser', email='test@example.com')
    user.save()
    
    with pytest.raises(FieldError, match="Related Field got invalid lookup: exact"):
        query.build_filter(('email__icontains', 'test'))