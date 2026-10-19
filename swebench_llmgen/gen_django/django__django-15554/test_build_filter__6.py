import pytest
from django.db.models import Q
from django.db.models.sql.query import Query
from django.contrib.auth.models import User
from django.core.exceptions import FieldError, TypeError

def test_build_filter_dict_expression():
    query = Query()
    with pytest.raises(FieldError, match="Cannot parse keyword query as dict"):
        query.build_filter({'username': 'testuser'})

def test_build_filter_q_expression():
    query = Query()
    filter_expr = Q(username='testuser')
    clause, used_joins = query.build_filter(filter_expr)
    assert clause is not None
    assert len(used_joins) == 0

def test_build_filter_non_conditional_expression():
    class NonConditionalExpression:
        conditional = False
        
    query = Query()
    with pytest.raises(TypeError, match="Cannot filter against a non-conditional expression."):
        query.build_filter(NonConditionalExpression())

def test_build_filter_valid_expression():
    query = Query()
    clause, used_joins = query.build_filter(('username', 'testuser'))
    assert clause is not None
    assert used_joins is not None

def test_build_filter_empty_arg():
    query = Query()
    with pytest.raises(FieldError, match="Cannot parse keyword query None"):
        query.build_filter((None, 'testuser'))

def test_build_filter_invalid_lookup():
    query = Query()
    with pytest.raises(FieldError, match="Related Field got invalid lookup: exact"):
        query.build_filter(('related_field__invalid_lookup', 'value'))

def test_build_filter_branch_negated():
    query = Query()
    filter_expr = Q(username='testuser')
    clause, used_joins = query.build_filter(filter_expr, branch_negated=True)
    assert clause is not None
    assert 'username' in str(clause)

def test_build_filter_current_negated():
    query = Query()
    filter_expr = Q(username='testuser')
    clause, used_joins = query.build_filter(filter_expr, current_negated=True)
    assert clause is not None
    assert 'username' in str(clause)

def test_build_filter_no_joins():
    query = Query()
    clause, used_joins = query.build_filter(('username', 'testuser'), allow_joins=False)
    assert clause is not None
    assert len(used_joins) == 0