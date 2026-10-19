import pytest
from django.db.models.expressions import BaseExpression
from django.contrib.auth.models import User

class TestBaseExpression(BaseExpression):

    def __init__(self, output_field):
        super().__init__(output_field)
        self.source_expressions = []

    def get_source_expressions(self):
        return self.source_expressions

    def set_source_expressions(self, exprs):
        self.source_expressions = exprs

    def copy(self):
        return TestBaseExpression(self.output_field)

def test_relabeled_clone_with_non_empty_change_map():
    base_expr = TestBaseExpression(output_field='some_field')
    base_expr.set_source_expressions([
        TestBaseExpression(output_field='another_field'),
        TestBaseExpression(output_field='yet_another_field')
    ])
    
    change_map = {
        'some_field': 'new_some_field',
        'another_field': 'new_another_field',
    }

    cloned_expr = base_expr.relabeled_clone(change_map)

    assert cloned_expr.get_source_expressions()[0].output_field == 'new_another_field'
    assert cloned_expr.get_source_expressions()[1].output_field == 'yet_another_field'

def test_relabeled_clone_without_change_map():
    base_expr = TestBaseExpression(output_field='some_field')
    base_expr.set_source_expressions([
        TestBaseExpression(output_field='another_field'),
    ])

    change_map = {}

    cloned_expr = base_expr.relabeled_clone(change_map)

    assert cloned_expr.get_source_expressions()[0].output_field == 'another_field'

def test_relabeled_clone_with_none_source_expression():
    base_expr = TestBaseExpression(output_field='some_field')
    base_expr.set_source_expressions([None])

    change_map = {
        'some_field': 'new_some_field',
    }

    cloned_expr = base_expr.relabeled_clone(change_map)

    assert cloned_expr.get_source_expressions() == [None]