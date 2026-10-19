import pytest
from django.core.exceptions import FieldError
from django.db.models import Aggregate
from django.db.models.functions import Coalesce
from django.db.models.expressions import F
from django.contrib.auth.models import User

class CustomAggregate(Aggregate):
    def resolve_expression(self, query=None, allow_joins=True, reuse=None, summarize=False, for_save=False):
        c = super().resolve_expression(query, allow_joins, reuse, summarize)
        c.filter = c.filter and c.filter.resolve_expression(query, allow_joins, reuse, summarize)
        if not summarize:
            expressions = super(CustomAggregate, c).get_source_expressions()
            for index, expr in enumerate(expressions):
                if expr.contains_aggregate:
                    before_resolved = self.get_source_expressions()[index]
                    name = before_resolved.name if hasattr(before_resolved, 'name') else repr(before_resolved)
                    raise FieldError("Cannot compute %s('%s'): '%s' is an aggregate" % (c.name, name, name))
        if (default := c.default) is None:
            return c
        if hasattr(default, 'resolve_expression'):
            default = default.resolve_expression(query, allow_joins, reuse, summarize)
        c.default = None  # Reset the default argument before wrapping.
        return Coalesce(c, default, output_field=c._output_field_or_none)

def test_resolve_expression_with_valid_aggregate():
    aggregate = CustomAggregate()
    user = User.objects.create(username='testuser')
    result = aggregate.resolve_expression()
    assert isinstance(result, Coalesce)

def test_resolve_expression_with_aggregate_in_expression():
    aggregate = CustomAggregate()
    user = User.objects.create(username='testuser')
    aggregate.set_source_expressions([F('id'), aggregate])  # Intentionally causing an aggregate to be part of source expressions
    with pytest.raises(FieldError) as excinfo:
        aggregate.resolve_expression()
    assert "is an aggregate" in str(excinfo.value)

def test_resolve_expression_with_default_value():
    default_value = 10
    aggregate = CustomAggregate()
    aggregate.default = default_value
    result = aggregate.resolve_expression()
    assert result.default == None  # Ensure default is reset before wrapping
    assert isinstance(result, Coalesce)

def test_resolve_expression_with_no_default():
    aggregate = CustomAggregate()
    aggregate.default = None
    result = aggregate.resolve_expression()
    assert result.default is None  # No default value should return None