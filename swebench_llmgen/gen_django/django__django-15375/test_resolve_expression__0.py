import pytest
from django.core.exceptions import FieldError
from django.db.models import Aggregate, IntegerField
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User

class CustomAggregate(Aggregate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, output_field=IntegerField(), **kwargs)

def test_resolve_expression_no_summary():
    aggregate = CustomAggregate('some_field')
    resolved_expr = aggregate.resolve_expression()

    assert resolved_expr is not None
    assert resolved_expr.__class__ == Coalesce

def test_resolve_expression_with_default():
    aggregate = CustomAggregate('some_field', default=5)
    resolved_expr = aggregate.resolve_expression()

    assert resolved_expr is not None
    assert resolved_expr.default == 5

def test_resolve_expression_with_aggregate_in_expressions():
    aggregate = CustomAggregate('some_field')
    aggregate.set_source_expressions([CustomAggregate('other_field')])

    with pytest.raises(FieldError) as excinfo:
        aggregate.resolve_expression(summarize=False)

    assert "Cannot compute" in str(excinfo.value)

def test_resolve_expression_default_none():
    aggregate = CustomAggregate('some_field', default=None)
    resolved_expr = aggregate.resolve_expression()

    assert resolved_expr is not None
    assert resolved_expr.default is None