import pytest
from django.core.exceptions import FieldError
from django.db.models import Aggregate, F, Value
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User

class TestAggregate(Aggregate):
    template = 'some_template'

def test_resolve_expression_without_summarize():
    aggregate = TestAggregate(F('id'))
    expression = aggregate.resolve_expression()

    assert expression is not None
    assert expression.template == 'some_template'
    assert expression.default is None

def test_resolve_expression_with_default():
    aggregate = TestAggregate(F('id'))
    aggregate.default = Value(1)
    expression = aggregate.resolve_expression()

    assert expression is not None
    assert isinstance(expression, Coalesce)
    assert expression.default == 1

def test_resolve_expression_with_aggregate_in_expressions():
    aggregate = TestAggregate(F('id'))
    aggregate.set_source_expressions([TestAggregate(F('id'))])  # setting same aggregate in source expressions
    
    with pytest.raises(FieldError, match=r"Cannot compute .*: '.*' is an aggregate"):
        aggregate.resolve_expression()

def test_resolve_expression_with_summarize():
    aggregate = TestAggregate(F('id'))
    expression = aggregate.resolve_expression(summarize=True)

    assert expression is not None
    assert expression.template == 'some_template'

def test_resolve_expression_with_complex_default():
    user = User.objects.create(username='testuser')
    aggregate = TestAggregate(F('id'))
    aggregate.default = Value(user.id)  # set the default as a user ID
    expression = aggregate.resolve_expression()

    assert expression is not None
    assert isinstance(expression, Coalesce)
    assert expression.default == user.id