import pytest
from django.db.models import Value
from django.db.models.expressions import BaseExpression
from django.db.models import OrderBy
from django.contrib.auth.models import User

class TestBaseExpression:
    def test_desc(self):
        # Create an instance of BaseExpression
        expression = BaseExpression(Value(1))

        # Call the desc method
        result = expression.desc()

        # Ensure the result is an instance of OrderBy with descending set to True
        assert isinstance(result, OrderBy)
        assert result.descending is True

        # Check if the expression used in OrderBy is the same as the original expression
        assert result.get_source_expressions()[0] is expression