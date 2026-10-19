import math
from django.db import connection
from django.db.models import FloatField
from django.db.models.expressions import Func
from django.contrib.auth.models import User
import pytest

class Ceil(Func, FixDecimalInputMixin, NumericOutputFieldMixin):
    function = 'CEIL'
    output_field = FloatField()

    def as_oracle(self, compiler, connection, **extra_context):
        return super().as_sql(compiler, connection, function='CEIL', **extra_context)

@pytest.mark.parametrize("value, expected", [
    (1.1, 2.0),
    (1.5, 2.0),
    (2.0, 2.0),
    (-1.1, -1.0),
    (-1.5, -1.0),
    (-2.0, -2.0),
    (0, 0.0)
])
def test_ceil_as_oracle(value, expected):
    user = User(username="testuser", password="testpass")
    user.save()
    
    ceil_func = Ceil(value)
    sql, params = ceil_func.as_oracle(None, connection)

    assert "CEIL" in sql
    assert params == [value]

    cursor = connection.cursor()
    cursor.execute(sql, params)
    
    result = cursor.fetchone()[0]
    assert result == expected