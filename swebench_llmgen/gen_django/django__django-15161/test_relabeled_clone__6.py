import pytest
from django.db.models.expressions import BaseExpression
from django.contrib.auth.models import User

class TestBaseExpression(BaseExpression):
    def __init__(self, output_field=None):
        super().__init__(output_field)

    def copy(self):
        return TestBaseExpression(self.output_field)

    def get_source_expressions(self):
        return [self]

    def set_source_expressions(self, exprs):
        self.source_expressions = exprs

def test_relabeled_clone():
    expression = TestBaseExpression(output_field='field')
    change_map = {expression: 'new_field'}

    cloned_expression = expression.relabeled_clone(change_map)

    assert cloned_expression is not expression  # Ensure it's a new instance
    assert cloned_expression.output_field == 'field'  # Output field remains unchanged
    assert cloned_expression.get_source_expressions()[0] == change_map[expression]  # Source expression relabeled correctly