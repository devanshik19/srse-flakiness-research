import pytest
from django.contrib.auth.models import User
from django.db.models import F
from django.db.models.expressions import OrderBy
from django.db.models.expressions import BaseExpression

class TestBaseExpression:

    def test_desc(self):
        # Arrange
        base_expr = BaseExpression(output_field=F('username'))

        # Act
        order_by_desc = base_expr.desc()

        # Assert
        assert isinstance(order_by_desc, OrderBy)
        assert order_by_desc.expression == base_expr
        assert order_by_desc.descending is True

    def test_desc_with_kwargs(self):
        # Arrange
        base_expr = BaseExpression(output_field=F('username'))
        additional_arg = {'output_field': F('email')}

        # Act
        order_by_desc = base_expr.desc(**additional_arg)

        # Assert
        assert isinstance(order_by_desc, OrderBy)
        assert order_by_desc.expression == base_expr
        assert order_by_desc.descending is True
        assert order_by_desc.output_field == additional_arg['output_field']