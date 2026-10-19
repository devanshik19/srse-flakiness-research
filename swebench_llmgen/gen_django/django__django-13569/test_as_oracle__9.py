import math
import pytest
from django.db.models.expressions import Func
from django.db.models.fields import FloatField, IntegerField
from django.db.models.functions import Cast
from django.db.models.functions.mixins import FixDecimalInputMixin, NumericOutputFieldMixin
from django.db.models.lookups import Transform
from django.contrib.auth.models import User

class Ceil(Func, FixDecimalInputMixin, NumericOutputFieldMixin):
    def as_oracle(self, compiler, connection, **extra_context):
        return super().as_sql(compiler, connection, function='CEIL', **extra_context)

def test_as_oracle():
    # Prepare the user instance
    user = User.objects.create(username='testuser', password='password123')

    # Create an instance of the Ceil function
    ceil_function = Ceil(Cast(user.pk, FloatField()))

    # Utilize the ORM to compile the SQL
    from django.db import connection
    compiler = connection.ops.compiler
    sql, params = ceil_function.as_oracle(compiler, connection)

    # Verify the SQL output and parameters
    assert sql.lower().startswith("ceil(")
    assert sql.lower().endswith(")")
    assert len(params) == 1
    assert isinstance(params[0], float)  # Expecting the casted float of the user primary key