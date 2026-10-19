import pytest
from django.contrib.auth.models import User
from django.db.models import F
from django.db.models.expressions import BaseExpression

def test_copy_method():
    # Create an instance of BaseExpression using a simple subclass since BaseExpression itself cannot be instantiated
    class TestExpression(BaseExpression):
        def __init__(self, output_field):
            super().__init__(output_field)
            self.output_field = output_field

        def as_sql(self, compiler, connection):
            return 'SQL', []

        def get_db_converters(self, connection):
            return []

    original_expression = TestExpression(output_field=F('username'))
    
    # Perform the copy
    copied_expression = original_expression.copy()

    # Assert that the copied instance is not the same as the original (different objects in memory)
    assert copied_expression is not original_expression

    # Assert that the copied instance has the same output_field
    assert copied_expression.output_field == original_expression.output_field

    # Verify that the copy method creates a shallow copy (changing the original doesn't affect the copy)
    original_expression.output_field = F('email')
    assert copied_expression.output_field != original_expression.output_field

    # Ensure the copied expression is still an instance of TestExpression
    assert isinstance(copied_expression, TestExpression)