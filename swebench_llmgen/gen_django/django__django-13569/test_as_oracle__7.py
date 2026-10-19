import pytest
from django.db import connection
from django.db.models import F
from django.db.models.functions import Ceil
from django.contrib.auth.models import User

@pytest.mark.parametrize("value, expected", [
    (3.1, 4),
    (2.0, 2),
    (-2.5, -2),
    (0.0, 0),
])
def test_as_oracle(value, expected):
    # Create a User instance to ensure the database is used
    user = User.objects.create(username='testuser')

    # Prepare the query using the Ceil function
    ceil_value = Ceil(F('id'))  # Using id as a numeric field from the User model

    # Execute the query
    sql, params = ceil_value.as_oracle(None, connection)

    # Check the SQL and parameters
    assert "CEIL" in sql
    assert len(params) == 0  # There should be no parameters passed

    # Execute the query directly to verify the result
    result = User.objects.annotate(ceil_id=ceil_value).values_list('ceil_id', flat=True).first()
    
    # Check the expected result against the computed ceiling value
    assert result == expected