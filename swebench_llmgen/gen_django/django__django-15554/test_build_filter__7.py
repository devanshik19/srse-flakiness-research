import pytest
from django.db.models import Q
from django.db.models.sql.query import Query
from django.core.exceptions import FieldError, TypeError
from django.contrib.auth.models import User

@pytest.mark.parametrize("filter_expr, expected_exception", [
    ({"username": "testuser"}, FieldError),  # dict provided
    (Q(username="testuser"), None),          # valid Q object
    (User.username, None),                    # valid related expression
    (("", "testuser"), FieldError),          # empty arg
])
def test_build_filter_exceptions(filter_expr, expected_exception):
    query = Query User.objects.all())  # Initialize with a Query from User model
    if expected_exception:
        with pytest.raises(expected_exception):
            query.build_filter(filter_expr)
    else:
        result, used_joins = query.build_filter(filter_expr)
        assert result is not None
        assert used_joins is not None

def test_build_filter_with_valid_expression():
    query = Query(User.objects.all())  # Initialize with a Query from User model
    filter_expr = ("username", "testuser")
    result, used_joins = query.build_filter(filter_expr)
    
    assert result is not None
    assert isinstance(result, WhereNode)
    assert used_joins == set()  # No joins should be used in this simple case

def test_build_filter_with_negation():
    query = Query(User.objects.all())  # Initialize with a Query from User model
    filter_expr = Q(username="testuser")
    result, used_joins = query.build_filter(filter_expr, branch_negated=True, current_negated=False)
    
    assert result is not None
    assert isinstance(result, WhereNode)
    assert len(result.children) > 0  # There should be a condition added