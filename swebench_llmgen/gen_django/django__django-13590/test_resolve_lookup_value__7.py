import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query
from django.db.models import F

class TestQuery:

    @pytest.fixture
    def query(self):
        return Query(model=User, where=None, alias_cols=None)

    def test_resolve_lookup_value_with_resolvable_expression(self, query):
        class ResolvableExpression:
            def resolve_expression(self, query, reuse, allow_joins):
                return "resolved_value"

        resolved_value = query.resolve_lookup_value(ResolvableExpression(), can_reuse=True, allow_joins=True)
        assert resolved_value == "resolved_value"

    def test_resolve_lookup_value_with_list(self, query):
        values = [1, 2, 3]
        resolved_values = query.resolve_lookup_value(values, can_reuse=True, allow_joins=True)
        assert resolved_values == values

    def test_resolve_lookup_value_with_tuple(self, query):
        values = (4, 5, 6)
        resolved_values = query.resolve_lookup_value(values, can_reuse=True, allow_joins=True)
        assert resolved_values == values

    def test_resolve_lookup_value_with_nested_expressions(self, query):
        class NestedResolvableExpression:
            def resolve_expression(self, query, reuse, allow_joins):
                return "nested_resolved_value"
        
        values = [NestedResolvableExpression(), 7]
        resolved_values = query.resolve_lookup_value(values, can_reuse=True, allow_joins=True)
        assert resolved_values == ["nested_resolved_value", 7]

    def test_resolve_lookup_value_with_non_expression(self, query):
        value = 10
        resolved_value = query.resolve_lookup_value(value, can_reuse=True, allow_joins=True)
        assert resolved_value == 10