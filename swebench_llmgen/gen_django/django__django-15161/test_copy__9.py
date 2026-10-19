import copy
import pytest
from django.db.models import Expression
from django.contrib.auth.models import User

class TestBaseExpression:
    @pytest.fixture
    def base_expression(self):
        return Expression()  # Assuming Expression is the parent class and it initializes BaseExpression

    def test_copy(self, base_expression):
        copied_expression = base_expression.copy()
        
        # Check that the copy is a different object
        assert copied_expression is not base_expression
        
        # Check that the copied object is of the same type
        assert isinstance(copied_expression, type(base_expression))
        
        # Check that the attributes of the copied object are the same as the original
        for attr in base_expression.__dict__:
            assert getattr(copied_expression, attr) == getattr(base_expression, attr)