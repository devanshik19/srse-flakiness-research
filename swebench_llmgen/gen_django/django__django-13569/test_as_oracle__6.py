import math
import pytest
from django.db.models.expressions import Func
from django.db.models.fields import FloatField
from django.db.models.functions import Cast
from django.db.models.functions.math import Ceil
from django.contrib.auth.models import User

@pytest.mark.parametrize("value, expected", [
    (1.2, 2.0),
    (2.5, 3.0),
    (3.0, 3.0),
    (-1.2, -1.0),
    (-2.5, -2.0),
    (0.0, 0.0),
])
def test_as_oracle(value, expected, db):
    user = User.objects.create(username='testuser', password='password123')
    
    ceil_function = Ceil(Cast(user.id, FloatField()))
    sql, params = ceil_function.as_oracle(None, None)

    # Assuming the function is called correctly for expected values
    assert "CEIL" in sql
    assert ceil_function.as_sql(None, None) == ceil_function.as_oracle(None, None)
    
    # Check if the value passed through Ceil matches expected ceil result
    result = ceil_function.get_result_value(user.id)
    assert result == expected