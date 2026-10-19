import pytest
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression

class TestBaseExpression(BaseExpression):

    def __init__(self, output_field=None):
        super().__init__(output_field)

    def get_source_expressions(self):
        return []

    def set_source_expressions(self, exprs):
        pass

    def copy(self):
        return TestBaseExpression()

def test_relabeled_clone():
    # Create an instance of TestBaseExpression for testing
    original_expression = TestBaseExpression()

    # The change map to relabel the expressions
    change_map = {"old_label": "new_label"}
    
    # Call the relabeled_clone method
    cloned_expression = original_expression.relabeled_clone(change_map)

    # Validate the clone is not the same object as the original
    assert cloned_expression is not original_expression