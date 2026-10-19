import pytest
from django.contrib.auth.models import User
from django.db.models import F, Value
from django.db.models.expressions import BaseExpression

class TestBaseExpression(BaseExpression):
    def __init__(self, output_field):
        super().__init__(output_field)
        self._source_expressions = []

    def get_source_expressions(self):
        return self._source_expressions

    def set_source_expressions(self, exprs):
        self._source_expressions = exprs

    def copy(self):
        return TestBaseExpression(self.output_field)

def test_relabeled_clone():
    expr = TestBaseExpression(output_field=Value('test'))

    # Set up initial source expressions
    expr.set_source_expressions([F('username'), F('email')])

    # Create a change_map for relabelling
    change_map = {
        'username': 'user_name',
        'email': 'user_email'
    }

    # Clone the original expression with relabeling
    cloned_expr = expr.relabeled_clone(change_map)

    # Verify that the cloned expression has the correct relabeled source expressions
    relabeled_sources = cloned_expr.get_source_expressions()

    assert len(relabeled_sources) == 2
    assert relabeled_sources[0].name == 'user_name'
    assert relabeled_sources[1].name == 'user_email'