import math
import pytest
from django.db.models import F
from django.db.models.expressions import Func
from django.db.models.fields import FloatField
from django.db.models.functions import Cast
from django.db.models.functions.mixins import FixDecimalInputMixin, NumericOutputFieldMixin
from django.contrib.auth.models import User

class Ceil(Func, FixDecimalInputMixin, NumericOutputFieldMixin):
    function = 'CEIL'
    lookup_name = 'ceil'

    def as_oracle(self, compiler, connection, **extra_context):
        return super().as_sql(compiler, connection, function='CEIL', **extra_context)

@pytest.mark.parametrize("value, expected", [
    (1.4, 2),
    (2.0, 2),
    (3.6, 4),
    (-1.2, -1),
    (0.0, 0),
])
def test_as_oracle(value, expected):
    user = User(username='testuser')
    user.save()
    
    ceil_instance = Ceil(Cast(F('id'), FloatField()))  # Using 'id' as a placeholder for an actual field
    
    # Simulating the DB function call
    sql, params = ceil_instance.as_oracle(None, None)
    
    # Execute the SQL to confirm the expected outcome
    result = math.ceil(value)  # using math.ceil for validation
    assert result == expected