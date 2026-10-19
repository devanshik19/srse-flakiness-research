import copy
import pytest
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression

class TestBaseExpression(BaseExpression):

    def __init__(self, output_field=None):
        super().__init__(output_field)
        self.empty_result_set_value = None
        self.is_summary = False
        self._output_field_resolved_to_none = False
        self.filterable = True
        self.window_compatible = False

def test_copy():
    original_expr = TestBaseExpression(output_field='some_field')
    copied_expr = original_expr.copy()
    
    assert copied_expr is not original_expr  # Ensure it's a different instance
    assert copied_expr.output_field == original_expr.output_field  # Ensure output_field is copied
    assert copied_expr.empty_result_set_value == original_expr.empty_result_set_value  # Ensure empty_result_set_value is copied
    assert copied_expr.is_summary == original_expr.is_summary  # Ensure is_summary is copied
    assert copied_expr._output_field_resolved_to_none == original_expr._output_field_resolved_to_none  # Ensure _output_field_resolved_to_none is copied
    assert copied_expr.filterable == original_expr.filterable  # Ensure filterable is copied
    assert copied_expr.window_compatible == original_expr.window_compatible  # Ensure window_compatible is copied