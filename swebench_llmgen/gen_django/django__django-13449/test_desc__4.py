import pytest
from django.contrib.auth.models import User
from django.db.models import F
from django.db.models.expressions import OrderBy
from django.db.models.expressions import BaseExpression

class TestBaseExpression:

    def test_desc_returns_order_by_instance(self):
        expression = BaseExpression()
        order_by_expression = expression.desc()
        
        assert isinstance(order_by_expression, OrderBy)
        assert order_by_expression.expression == expression
        assert order_by_expression.descending is True

    def test_desc_with_kwargs(self):
        expression = BaseExpression()
        order_by_expression = expression.desc(nulls_first=True)
        
        assert isinstance(order_by_expression, OrderBy)
        assert order_by_expression.expression == expression
        assert order_by_expression.descending is True
        assert order_by_expression.nulls_first is True

    def test_desc_with_no_kwargs(self):
        expression = BaseExpression()
        order_by_expression = expression.desc()
        
        assert isinstance(order_by_expression, OrderBy)
        assert order_by_expression.nulls_first is None