import math
import pytest
from django.db import connection
from django.db.models.expressions import Func
from django.db.models.fields import FloatField, IntegerField
from django.db.models.functions import Cast
from django.db.models.functions.mixins import FixDecimalInputMixin, NumericOutputFieldMixin
from django.db.models.lookups import Transform
from django.contrib.auth.models import User

class Ceil(Func, FixDecimalInputMixin, NumericOutputFieldMixin):
    function = 'CEIL'
    lookup_name = 'ceil'

    def as_oracle(self, compiler, connection, **extra_context):
        return super().as_sql(compiler, connection, function='CEIL', **extra_context)

@pytest.mark.parametrize("input_value, expected_output", [
    (1.2, 2),
    (2.5, 3),
    (3.0, 3),
    (-1.5, -1),
    (-2.0, -2),
])
def test_as_oracle(input_value, expected_output):
    user = User.objects.create(username='testuser', password='testpass')
    ceil_function = Ceil(Cast(user.id, FloatField()))

    sql, params = ceil_function.as_oracle(None, connection)
    assert "CEIL" in sql
    assert params == [float(user.id)]

    ceil_result = connection.execute(sql, params).fetchall()
    assert ceil_result[0][0] == expected_output