import pytest
from django.contrib.auth.models import User
from django.db.models.expressions import CombinedExpression

def test_combined_expression_repr():
    lhs = User.objects.all()  # Using a queryset as the left-hand side
    rhs = User.objects.all()  # Using a queryset as the right-hand side
    connector = 'AND'  # Sample connector
    
    combined_expr = CombinedExpression(lhs, connector, rhs, output_field=None)
    
    # Test the repr output
    assert repr(combined_expr) == "<CombinedExpression: {}>".format(combined_expr)