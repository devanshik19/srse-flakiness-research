import pytest
from django.contrib.auth.models import User
from django.db.models.expressions import Func
from django.db.models.functions import Cast
from django.db.models import IntegerField
from django.db import connection
from django.db.models import F
from django.db.models.functions import Cast
from django.db.models.lookups import Transform

class Ceil(Func):
    fields = [FloatField()]
    lookup_name = 'ceil'

    def as_oracle(self, compiler, connection, **extra_context):
        return super().as_sql(compiler, connection, function='CEIL', **extra_context)

@pytest.mark.parametrize("input_value, expected_value", [
    (1.5, 2),
    (2.0, 2),
    (-1.5, -1),
    (-2.0, -2),
    (0.0, 0),
])
def test_ceil_as_oracle(input_value, expected_value):
    user = User.objects.create(username='testuser', password='password')
    ceil_func = Ceil(Cast(F('id'), IntegerField()))
    
    sql, params = ceil_func.as_oracle(connection.compiler('default'), connection)
    query = f"SELECT {sql} FROM auth_user WHERE id = %s"
    result = connection.execute(query, [user.id])
    
    assert result == expected_value