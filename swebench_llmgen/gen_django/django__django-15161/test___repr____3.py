import pytest
from django.db.models.expressions import CombinedExpression
from django.contrib.auth.models import User

def test_combined_expression_repr():
    lhs = User.objects.first()  # Get a user instance to serve as lhs
    rhs = User.objects.first()   # Get another user instance for rhs
    connector = 'AND'            # Example connector for CombinedExpression

    combined_expression = CombinedExpression(lhs, connector, rhs, output_field=None)
    expected_repr = "<CombinedExpression: {}>".format(combined_expression)
    
    assert repr(combined_expression) == expected_repr