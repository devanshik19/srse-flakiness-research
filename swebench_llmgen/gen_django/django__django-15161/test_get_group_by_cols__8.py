import pytest
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression


class TestBaseExpression(BaseExpression):
    def __init__(self, output_field=None, contains_aggregate=False):
        super().__init__(output_field)
        self._contains_aggregate = contains_aggregate

    def contains_aggregate(self):
        return self._contains_aggregate

    def get_source_expressions(self):
        return [self] if not self._contains_aggregate else []


@pytest.mark.parametrize(
    "contains_aggregate, expected_result",
    [
        (False, [TestBaseExpression()]),
        (True, [])
    ]
)
def test_get_group_by_cols(contains_aggregate, expected_result):
    expr = TestBaseExpression(contains_aggregate=contains_aggregate)
    result = expr.get_group_by_cols()
    assert result == expected_result