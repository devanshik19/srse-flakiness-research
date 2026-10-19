import pytest
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.expressions import OrderBy
from django.db.models.expressions import BaseExpression

class TestBaseExpression:

    def test_desc(self):
        expression = BaseExpression(output_field=None)
        order_by_expression = expression.desc()

        # Check that order_by_expression is an instance of OrderBy
        assert isinstance(order_by_expression, OrderBy)

        # Check that the expression is the original expression
        assert order_by_expression.targets[0] is expression

        # Check descending is True
        assert order_by_expression.descending is True

    def test_desc_with_kwargs(self):
        expression = BaseExpression(output_field=None)
        order_by_expression = expression.desc(nulls_first=True)

        # Check that order_by_expression carries the additional kwargs
        assert order_by_expression.nulls_first is True