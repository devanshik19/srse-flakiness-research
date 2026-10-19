import pytest
from django.db.models import Expression
from django.contrib.auth.models import User

class TestBaseExpression:

    def test_set_source_expressions_empty(self):
        expr = Expression()
        expr.set_source_expressions([])
        assert expr.get_source_expressions() == []

    def test_set_source_expressions_non_empty(self):
        expr = Expression()
        with pytest.raises(AssertionError):
            expr.set_source_expressions(['some_expression'])