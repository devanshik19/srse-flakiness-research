import pytest
from django.contrib.auth.models import User
from django.db.models.expressions import CombinedExpression

@pytest.mark.django_db
def test_combined_expression_repr():
    user = User.objects.create(username='testuser', password='password')
    lhs = user
    connector = "AND"
    rhs = user
    combined_expr = CombinedExpression(lhs, connector, rhs, output_field=None)

    expected_repr = "<CombinedExpression: {}>".format(combined_expr)
    assert repr(combined_expr) == expected_repr