import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.where import WhereNode
from django.db.models.fields.related_lookups import RelatedIn

@pytest.mark.parametrize("lhs_values, rhs_values, expected", [
    # Test case when lhs is MultiColSource and rhs is a direct value
    (
        User._meta.get_field('id'), 
        [1, 2], 
        "WHERE \"auth_user\".\"id\" IN (1, 2)"
    ),
    # Test case when lhs is MultiColSource and rhs is a SubqueryConstraint
    (
        User._meta.get_field('username'), 
        User.objects.filter(is_active=True), 
        "WHERE (Subquery Constraint)"
    ),
])
def test_as_sql(lhs_values, rhs_values, expected):
    related_in = RelatedIn(lhs=lhs_values, rhs=rhs_values)

    mock_compiler = None  # Replace with an actual compiler instance if needed
    mock_connection = None  # Replace with an actual connection instance if needed

    sql, params = related_in.as_sql(mock_compiler, mock_connection)

    assert sql == expected
    assert params == []