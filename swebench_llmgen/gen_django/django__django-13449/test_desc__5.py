import pytest
from django.db.models import F
from django.db.models.expressions import BaseExpression
from django.db.models import OrderBy
from django.contrib.auth.models import User

class TestBaseExpression:
    def test_desc(self):
        # Create an instance of the BaseExpression or subclass it
        expression = BaseExpression(output_field=None)

        # Call the desc method
        result = expression.desc()

        # Assert the result is an instance of OrderBy
        assert isinstance(result, OrderBy)

        # Check that the descending argument is set to True
        assert result.descending is True

        # Further check if the source expression is set correctly
        assert result.source == expression