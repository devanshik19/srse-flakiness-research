import pytest
from django.db.models import F
from django.db.models.expressions import OrderBy
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression

class TestBaseExpression:

    def test_desc(self):
        expression = BaseExpression(output_field=None)
        order_by_expression = expression.desc()  # Calling the desc() method

        assert isinstance(order_by_expression, OrderBy)
        assert order_by_expression.expression is expression
        assert order_by_expression.descending is True