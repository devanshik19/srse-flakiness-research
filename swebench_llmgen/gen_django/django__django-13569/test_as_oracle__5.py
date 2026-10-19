import math
import pytest
from django.db.models import Func
from django.db.models.fields import FloatField
from django.db.models.functions import Cast
from django.db.models import ExpressionWrapper
from django.contrib.auth.models import User
from django.db import connection

class Ceil(Func):
    function = 'CEIL'
    output_field = FloatField()

    def as_oracle(self, compiler, connection, **extra_context):
        return super().as_sql(compiler, connection, function='CEIL', **extra_context)

def test_ceil_as_oracle():
    ceil_instance = Ceil(ExpressionWrapper(1.5, output_field=FloatField()))
    
    # Assuming compiler and connection can be obtained via the Django ORM
    compiler = connection.scheduler.compile(ceil_instance)
    
    sql, params = ceil_instance.as_oracle(compiler, connection)
    
    assert sql == 'CEIL(%s)'
    assert params == [1.5]

    # Test on a real User model instance
    user = User.objects.create(username='testuser', password='testpass')
    
    ceil_value = Ceil(Cast(user.id, FloatField()))
    sql, params = ceil_value.as_oracle(compiler, connection)
    
    assert sql.startswith('CEIL(CAST(')
    assert 'AS FLOAT' in sql