import pytest
from django.contrib.auth.models import User
from django.db.models.expressions import CombinedExpression

def test_combined_expression_repr():
    lhs = User.objects.first()  # Assuming at least one User object exists
    connector = 'AND'  # Example connector
    rhs = User.objects.filter(is_active=True)  # Example rhs expression
    output_field = None  # Assuming no output field for this test

    combined_expr = CombinedExpression(lhs, connector, rhs, output_field)

    expected_repr = "<CombinedExpression: {}>".format(combined_expr)
    assert repr(combined_expr) == expected_repr