import pytest
from django.db.models.sql.query import Query
from django.contrib.auth.models import User

class TestQueryResolveLookupValue:

    @pytest.fixture(autouse=True)
    def setup_method(self):
        # Mock the Query class for testing
        self.query = Query(User._meta)

    def test_resolve_lookup_value_with_resolvable_expression(self):
        class MockExpression:
            def resolve_expression(self, query, reuse, allow_joins):
                return 'resolved_value'
        
        result = self.query.resolve_lookup_value(MockExpression(), True, True)
        assert result == 'resolved_value'

    def test_resolve_lookup_value_with_list(self):
        result = self.query.resolve_lookup_value([1, 2, MockExpression()], True, True)
        assert result == [1, 2, 'resolved_value']

    def test_resolve_lookup_value_with_tuple(self):
        result = self.query.resolve_lookup_value((MockExpression(), 3), True, True)
        assert result == ['resolved_value', 3]

    def test_resolve_lookup_value_with_non_expression(self):
        result = self.query.resolve_lookup_value('non_expression_value', True, True)
        assert result == 'non_expression_value'

    def test_resolve_lookup_value_with_empty_list(self):
        result = self.query.resolve_lookup_value([], True, True)
        assert result == []

    def test_resolve_lookup_value_with_empty_tuple(self):
        result = self.query.resolve_lookup_value((), True, True)
        assert result == ()