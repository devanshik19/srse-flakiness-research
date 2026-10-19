import pytest
from django.db.models import F
from django.db.models.expressions import BaseExpression
from django.db.models import OrderBy
from django.contrib.auth.models import User

class TestBaseExpression:
    
    def test_desc(self):
        # Arrange
        expression = BaseExpression(output_field=F('id'))
        
        # Act
        result = expression.desc()

        # Assert
        assert isinstance(result, OrderBy)
        assert result.expr == expression
        assert result.descending is True