import pytest
from django.core.exceptions import FieldError
from django.db.models import Aggregate, F
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User

class TestAggregate(Aggregate):
    def get_source_expressions(self):
        return [F('id')]

def test_resolve_expression_no_default():
    aggregate = TestAggregate()
    resolved = aggregate.resolve_expression()
    assert resolved is not None
    assert resolved.default is None

def test_resolve_expression_with_default():
    aggregate = TestAggregate(default=1)
    resolved = aggregate.resolve_expression()
    assert isinstance(resolved, Coalesce)
    assert resolved.default == 1

def test_resolve_expression_with_aggregate_in_expressions():
    aggregate = TestAggregate()
    aggregate.set_source_expressions([TestAggregate()])
    
    with pytest.raises(FieldError) as excinfo:
        aggregate.resolve_expression()
    assert "Cannot compute" in str(excinfo.value)

def test_resolve_expression_with_filter():
    aggregate = TestAggregate()
    aggregate.filter = TestAggregate()  # Setting some filter for testing

    resolved = aggregate.resolve_expression()
    assert resolved.filter is not None