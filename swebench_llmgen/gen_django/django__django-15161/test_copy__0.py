import pytest
import copy
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression

class TestBaseExpression:

    @pytest.fixture
    def base_expression(self):
        return BaseExpression(output_field=None)

    def test_copy(self, base_expression):
        copied_expression = base_expression.copy()
        assert copied_expression is not base_expression  # Ensure it's a new object
        assert copied_expression == base_expression  # Ensure the contents are the same

    def test_copy_is_instance(self, base_expression):
        copied_expression = base_expression.copy()
        assert isinstance(copied_expression, BaseExpression)  # Ensure it is an instance of BaseExpression