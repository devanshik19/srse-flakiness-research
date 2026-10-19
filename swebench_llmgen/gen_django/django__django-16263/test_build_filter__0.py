import pytest
from django.db.models import Q
from django.db.models.sql.query import Query
from django.contrib.auth.models import User
from django.core.exceptions import FieldError, TypeError

@pytest.fixture
def query_instance():
    return Query(User._meta)

def test_build_filter_with_valid_dict(query_instance):
    filter_expr = {'username': 'testuser'}
    clause, used_joins = query_instance.build_filter(filter_expr)
    assert clause is not None
    assert len(used_joins) >= 0

def test_build_filter_with_valid_q_object(query_instance):
    filter_expr = Q(username='testuser')
    clause, used_joins = query_instance.build_filter(filter_expr)
    assert clause is not None
    assert len(used_joins) >= 0

def test_build_filter_with_expression(query_instance):
    from django.db.models import F
    filter_expr = F('username')
    clause, used_joins = query_instance.build_filter((filter_expr, 'testuser'))
    assert clause is not None
    assert len(used_joins) >= 0

def test_build_filter_with_empty_arg(query_instance):
    with pytest.raises(FieldError):
        query_instance.build_filter(('', 'value'))

def test_build_filter_with_non_conditional_expression(query_instance):
    from django.db.models import Value
    filter_expr = Value('testvalue')
    with pytest.raises(TypeError):
        query_instance.build_filter(filter_expr)

def test_build_filter_with_invalid_dict(query_instance):
    filter_expr = {'invalid_field': 'value'}
    with pytest.raises(FieldError):
        query_instance.build_filter(filter_expr)

def test_build_filter_with_branch_negated(query_instance):
    filter_expr = Q(username='testuser')
    clause, used_joins = query_instance.build_filter(filter_expr, branch_negated=True)
    assert clause is not None
    assert len(used_joins) >= 0

def test_build_filter_with_current_negated(query_instance):
    filter_expr = Q(username='testuser')
    clause, used_joins = query_instance.build_filter(filter_expr, current_negated=True)
    assert clause is not None
    assert len(used_joins) >= 0