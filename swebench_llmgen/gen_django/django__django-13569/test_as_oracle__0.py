import pytest
from django.db import connection
from django.db.models import Func, F
from django.contrib.auth.models import User

class Ceil(Func):
    def as_oracle(self, compiler, connection, **extra_context):
        return super().as_sql(compiler, connection, function='CEIL', **extra_context)

def test_ceil_as_oracle():
    # Create a user instance to ensure database access
    user = User.objects.create(username='testuser', password='password')

    # Use the custom Ceil function
    ceil_expr = Ceil(F('id'))  # Using user id for demonstration

    # Fetch SQL from as_oracle
    sql, params = ceil_expr.as_oracle(connection.ops.compiler, connection)

    # Validate the generated SQL
    assert 'CEIL' in sql
    assert 'testuser' in str(params)  # just looking for a placeholder in params

    # Execute the SQL directly to validate if it returns the expected results
    result = connection.cursor().execute(sql, params)
    assert result is not None