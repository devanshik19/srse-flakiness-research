import pytest
from django.db.models import Q
from django.core.exceptions import FieldError
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

@pytest.mark.parametrize(
    "filter_expr, expected_exception",
    [
        ({'invalid_field': 'value'}, FieldError),
        (Q(invalid_field='value'), FieldError),
        (('valid_field', 'value'), None),
    ]
)
def test_build_filter_exceptions(filter_expr, expected_exception):
    query = Query(model=User)
    
    if expected_exception:
        with pytest.raises(expected_exception):
            query.build_filter(filter_expr)
    else:
        result, used_joins = query.build_filter(filter_expr)
        assert result is not None
        assert isinstance(result, tuple)

def test_build_filter_with_q_expression():
    query = Query(model=User)
    q_expression = Q(username='testuser')
    result, used_joins = query.build_filter(q_expression)
    
    assert result is not None
    assert isinstance(result, tuple)

def test_build_filter_with_nested_q_expression():
    query = Query(model=User)
    q_expression = Q(username='testuser') | Q(email='testuser@example.com')
    result, used_joins = query.build_filter(q_expression)
    
    assert result is not None
    assert isinstance(result, tuple)

def test_build_filter_with_valid_expression():
    query = Query(model=User)
    filter_expr = ('username', 'testuser')
    result, used_joins = query.build_filter(filter_expr)
    
    assert result is not None
    assert isinstance(result, tuple)