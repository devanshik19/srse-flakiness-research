import pytest
from django.db.models import Expression
from django.contrib.auth.models import User

class BaseExpression(Expression):
    def set_source_expressions(self, exprs):
        assert not exprs

def test_set_source_expressions_empty():
    expr = BaseExpression(output_field=None)
    expr.set_source_expressions([])  # Should not raise an assertion error

def test_set_source_expressions_non_empty():
    expr = BaseExpression(output_field=None)
    
    with pytest.raises(AssertionError):
        expr.set_source_expressions([User.objects.create(username='testuser')])