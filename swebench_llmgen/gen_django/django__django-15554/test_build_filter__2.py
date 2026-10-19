import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query
from django.db.models import Q
from django.core.exceptions import FieldError, TypeError


@pytest.fixture
def query():
    return Query(model=User, alias_cols=None)  # Replace with actual initialization as needed


def test_build_filter_dict_raises_fielderror(query):
    with pytest.raises(FieldError, match="Cannot parse keyword query as dict"):
        query.build_filter({"username": "testuser"})


def test_build_filter_q_instance(query):
    filter_expr = Q(username="testuser")
    clause, used_joins = query.build_filter(filter_expr)
    assert clause is not None
    assert len(used_joins) > 0  # Check if joins were used


def test_build_filter_non_conditional_expression_raises_typeerror(query):
    class NonConditionalExpression:
        conditional = False

        def resolve_expression(self, *args, **kwargs):
            return self

    with pytest.raises(TypeError, match="Cannot filter against a non-conditional expression."):
        query.build_filter(NonConditionalExpression())


def test_build_filter_empty_arg_raises_fielderror(query):
    with pytest.raises(FieldError, match="Cannot parse keyword query None"):
        query.build_filter((None, "value"))


def test_build_filter_invalid_lookup_raises_fielderror(query):
    with pytest.raises(FieldError, match="Related Field got invalid lookup: exact"):
        query.build_filter(("invalid_field__exact", "value"))


def test_build_filter_raises_fielderror_for_joined_fields(query):
    with pytest.raises(FieldError, match="Joined field references are not permitted in this query"):
        query.build_filter(("related_model__field", "value"), allow_joins=False)


def test_build_filter_successful_filter(query):
    clause, used_joins = query.build_filter(("username", "testuser"))
    assert clause is not None
    assert used_joins is not None


def test_build_filter_with_negation(query):
    clause, used_joins = query.build_filter(("username", "testuser"), current_negated=True)
    assert clause is not None
    assert used_joins is not None


def test_build_filter_with_multiple_lookups(query):
    clause, used_joins = query.build_filter(("username__iexact", "testuser"))
    assert clause is not None
    assert used_joins is not None