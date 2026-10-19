import copy
import pytest
from django.db.models.expressions import BaseExpression
from django.contrib.auth.models import User

class TestBaseExpression(BaseExpression):
    def __init__(self, output_field=None):
        super().__init__(output_field=output_field)
        self.source_expressions = []

    def get_source_expressions(self):
        return self.source_expressions

    def set_source_expressions(self, exprs):
        self.source_expressions = exprs

    def copy(self):
        return copy.deepcopy(self)

def test_relabeled_clone_empty_source_expressions():
    expression = TestBaseExpression()
    change_map = {}
    cloned_expression = expression.relabeled_clone(change_map)
    
    assert cloned_expression.get_source_expressions() == []
    assert cloned_expression is not expression

def test_relabeled_clone_single_source_expression():
    expression = TestBaseExpression()
    sub_expression = TestBaseExpression()
    expression.set_source_expressions([sub_expression])
    
    change_map = {}
    cloned_expression = expression.relabeled_clone(change_map)
    
    assert len(cloned_expression.get_source_expressions()) == 1
    assert cloned_expression.get_source_expressions()[0] is not sub_expression
    assert cloned_expression.get_source_expressions()[0].get_source_expressions() == []

def test_relabeled_clone_multiple_source_expressions():
    expression = TestBaseExpression()
    sub_expression1 = TestBaseExpression()
    sub_expression2 = TestBaseExpression()
    expression.set_source_expressions([sub_expression1, sub_expression2])
    
    change_map = {}
    cloned_expression = expression.relabeled_clone(change_map)
    
    assert len(cloned_expression.get_source_expressions()) == 2
    assert cloned_expression.get_source_expressions()[0] is not sub_expression1
    assert cloned_expression.get_source_expressions()[1] is not sub_expression2
    assert cloned_expression.get_source_expressions()[0].get_source_expressions() == []
    assert cloned_expression.get_source_expressions()[1].get_source_expressions() == []

def test_relabeled_clone_with_change_map():
    expression = TestBaseExpression()
    sub_expression1 = TestBaseExpression()
    expression.set_source_expressions([sub_expression1])
    
    change_map = {id(sub_expression1): TestBaseExpression()}  # Change to a new instance
    cloned_expression = expression.relabeled_clone(change_map)
    
    assert len(cloned_expression.get_source_expressions()) == 1
    assert cloned_expression.get_source_expressions()[0] is not sub_expression1
    assert id(cloned_expression.get_source_expressions()[0]) in change_map.values()