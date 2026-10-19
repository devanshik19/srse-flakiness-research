import pytest
from django.db.models import Expression
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression

class TestBaseExpression(BaseExpression):

    def set_source_expressions(self, exprs):
        assert not exprs

def test_set_source_expressions_empty():
    expression = TestBaseExpression(output_field=F('username'))
    expression.set_source_expressions([])

def test_set_source_expressions_non_empty():
    expression = TestBaseExpression(output_field=F('username'))
    with pytest.raises(AssertionError):
        expression.set_source_expressions([F('email')])