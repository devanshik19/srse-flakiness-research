import pytest
from django.contrib.auth.models import User
from django.db.models.expressions import CombinedExpression

def test_combined_expression_repr():
    user = User.objects.create_user(username='testuser', password='testpass')
    lhs = CombinedExpression(User.username, 'AND', user.username, output_field=None)
    
    expected_repr = "<CombinedExpression: <CombinedExpression: {}>>".format(lhs)
    assert repr(lhs) == expected_repr