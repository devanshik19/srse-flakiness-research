import pytest
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression

class TestBaseExpression(BaseExpression):
    def __init__(self, output_field=None):
        super().__init__(output_field)
        self.source_expressions = []

    def get_source_expressions(self):
        return self.source_expressions

    def set_source_expressions(self, exprs):
        self.source_expressions = exprs

    def copy(self):
        return TestBaseExpression()

def test_relabeled_clone_with_single_expression():
    expression = TestBaseExpression()
    expression.set_source_expressions([TestBaseExpression()])
    
    change_map = {id(expression.get_source_expressions()[0]): TestBaseExpression()}
    
    cloned_expression = expression.relabeled_clone(change_map)
    
    assert cloned_expression is not expression
    assert len(cloned_expression.get_source_expressions()) == 1
    assert cloned_expression.get_source_expressions()[0] is not expression.get_source_expressions()[0]
    
def test_relabeled_clone_with_no_expression():
    expression = TestBaseExpression()
    expression.set_source_expressions([None])
    
    change_map = {}
    
    cloned_expression = expression.relabeled_clone(change_map)
    
    assert cloned_expression is not expression
    assert cloned_expression.get_source_expressions() == [None]
    
def test_relabeled_clone_with_multiple_expressions():
    expression = TestBaseExpression()
    expression.set_source_expressions([TestBaseExpression(), TestBaseExpression()])
    
    change_map = {
        id(expression.get_source_expressions()[0]): TestBaseExpression(),
        id(expression.get_source_expressions()[1]): TestBaseExpression()
    }
    
    cloned_expression = expression.relabeled_clone(change_map)
    
    assert cloned_expression is not expression
    assert len(cloned_expression.get_source_expressions()) == 2
    for orig, clone in zip(expression.get_source_expressions(), cloned_expression.get_source_expressions()):
        assert clone is not orig