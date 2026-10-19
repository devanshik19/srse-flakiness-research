import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.exceptions import FieldError, TypeError
from django.db.models.sql.query import Query

@pytest.mark.parametrize("filter_expr, expected_exception", [
    ({"username": "test"}, FieldError),  # dict case
    (Q(username="test") & Q(email="test@example.com"), None),  # valid Q object
    (Q(username="test", email="test@example.com"), None),  # valid Q object with multiple conditions
    ("username", FieldError),  # missing value
    (("username", None), None),  # valid lookup with None
])
def test_build_filter_exceptions(filter_expr, expected_exception):
    query = Query(User)  # Using the User model

    if expected_exception:
        with pytest.raises(expected_exception):
            query.build_filter(filter_expr)
    else:
        clause, used_joins = query.build_filter(filter_expr)
        assert clause is not None  # Ensure the clause is built correctly
        assert isinstance(clause, WhereNode)  # Check correct return type


def test_build_filter_with_valid_expression():
    query = Query(User)
    clause, used_joins = query.build_filter(("username", "testuser"))  # valid case
    assert clause is not None
    assert isinstance(clause, WhereNode)
    assert len(clause.children) == 1


def test_build_filter_with_non_conditional_expression():
    query = Query(User)
    with pytest.raises(TypeError) as excinfo:
        query.build_filter(F("username"))  # F expression not conditional
    assert "Cannot filter against a non-conditional expression." in str(excinfo.value)


def test_build_filter_with_join_not_allowed():
    query = Query(User)
    with pytest.raises(FieldError) as excinfo:
        query.build_filter(("profile__bio", "testbio"), allow_joins=False)  # joined field reference not allowed
    assert "Joined field references are not permitted in this query" in str(excinfo.value)


def test_build_filter_with_reusable_joins():
    query = Query(User)
    can_reuse = set()
    clause, used_joins = query.build_filter(("username", "testuser"), can_reuse=can_reuse)
    assert used_joins == set()  # No joins should be used for this simple lookup