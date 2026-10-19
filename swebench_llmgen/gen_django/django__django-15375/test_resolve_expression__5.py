import pytest
from django.core.exceptions import FieldError
from django.db.models import Aggregate, IntegerField, Func, Case, When
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User

class TestAggregate(Aggregate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_source_expressions(self):
        # Example expressions for testing
        return [self]

@pytest.fixture
def aggregate_instance():
    return TestAggregate()

def test_resolve_expression_default_none(aggregate_instance):
    resolved = aggregate_instance.resolve_expression()
    assert resolved is not None
    assert resolved.default is None

def test_resolve_expression_with_default(aggregate_instance):
    aggregate_instance.default = 5
    resolved = aggregate_instance.resolve_expression()
    assert isinstance(resolved, Coalesce)
    assert resolved.default == 5

def test_resolve_expression_aggregate_field_error(aggregate_instance):
    # Simulating an aggregate expression
    aggregate_instance.set_source_expressions([aggregate_instance])
    with pytest.raises(FieldError, match="Cannot compute"):
        aggregate_instance.resolve_expression(summarize=False)