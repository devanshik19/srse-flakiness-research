import pytest
from django.db.models import Expression
from django.contrib.auth.models import User

class BaseExpression(Expression):
    def set_source_expressions(self, exprs):
        assert not exprs

def test_set_source_expressions_with_empty_exprs():
    expr = BaseExpression(output_field=None)
    expr.set_source_expressions([])  # Should pass as exprs is an empty list

def test_set_source_expressions_with_non_empty_exprs():
    expr = BaseExpression(output_field=None)
    with pytest.raises(AssertionError):
        expr.set_source_expressions([User])  # Should raise an AssertionError since exprs is not empty