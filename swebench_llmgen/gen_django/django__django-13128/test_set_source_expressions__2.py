import pytest
from django.db.models import fields
from django.contrib.auth.models import User
from yourapp.models import BaseExpression

class TestBaseExpression:
    def test_set_source_expressions_empty(self):
        expr = BaseExpression(output_field=fields.CharField())
        expr.set_source_expressions([])  # should pass without error

    def test_set_source_expressions_non_empty(self):
        expr = BaseExpression(output_field=fields.CharField())
        with pytest.raises(AssertionError):
            expr.set_source_expressions([User.objects.first()])  # should raise AssertionError