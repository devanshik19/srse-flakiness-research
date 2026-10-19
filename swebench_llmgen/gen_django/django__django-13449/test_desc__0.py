import pytest
from django.db.models import F
from django.db.models import OrderBy
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression

class TestBaseExpression:

    def test_desc_method(self):
        expression = BaseExpression(output_field=None)  # Assuming output_field is None for test
        order_by_expression = expression.desc()

        assert isinstance(order_by_expression, OrderBy)
        assert order_by_expression.get_source_expressions()[0] == expression
        assert order_by_expression.descending is True

    def test_desc_with_kwargs(self):
        expression = BaseExpression(output_field=None)
        order_by_expression = expression.desc(nulls_first=True)

        assert isinstance(order_by_expression, OrderBy)
        assert order_by_expression.get_source_expressions()[0] == expression
        assert order_by_expression.descending is True
        assert order_by_expression.nulls_first is True