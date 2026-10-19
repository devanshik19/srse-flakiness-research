import pytest
from django.db.models import F
from django.db.models.expressions import BaseExpression
from django.db.models import OrderBy
from django.contrib.auth.models import User

class TestBaseExpression:

    def test_desc_ordering(self):
        # Create an instance of BaseExpression (using a relevant field for demonstration)
        expression = BaseExpression()

        # Call the desc method
        order_by_desc = expression.desc(field=F('username'))

        # Verify that the result is an instance of OrderBy and check its ordering
        assert isinstance(order_by_desc, OrderBy)
        assert order_by_desc.expression == expression
        assert order_by_desc.descending is True
        assert order_by_desc.get_source_expressions() == [F('username')]