import pytest
from django.db.models.expressions import CombinedExpression
from django.contrib.auth.models import User

def test_combined_expression_repr():
    user = User(username='testuser')
    lhs = CombinedExpression(user.username, 'AND', 'other_value', output_field=None)
    
    # Test __repr__ output
    repr_output = repr(lhs)
    assert repr_output == "<CombinedExpression: <__main__.CombinedExpression object at 0x*>>"