import pytest
from django.contrib.auth.models import User
from django.db.models import DurationField
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.expressions import F
from django.db import connection

class DurationExpression:
    def compile(self, side, compiler, connection):
        try:
            output = side.output_field
        except FieldError:
            pass
        else:
            if output.get_internal_type() == 'DurationField':
                sql, params = compiler.compile(side)
                return connection.ops.format_for_duration_arithmetic(sql), params
        return compiler.compile(side)

@pytest.fixture
def duration_expression():
    return DurationExpression()

@pytest.fixture
def user_with_duration_field():
    user = User(username='testuser', first_name='Test', last_name='User')
    user.save()
    return user

def test_compile_with_duration_field(duration_expression, user_with_duration_field):
    duration_side = F('last_login')  # Assuming last_login is viewed as DurationField for this test
    compiler = SQLCompiler(connection=queryset.model)
    
    # Manually set output_field to simulate DurationField
    compiler.output_field = DurationField()
    
    sql, params = duration_expression.compile(duration_side, compiler, connection)
    
    assert isinstance(sql, str)
    assert params == []  # Adjust as needed based on the actual SQL and parameters used

def test_compile_without_duration_field(duration_expression):
    non_duration_side = F('username')  # Focusing on a non-DurationField attribute
    compiler = SQLCompiler(connection=queryset.model)

    sql, params = duration_expression.compile(non_duration_side, compiler, connection)
    
    assert isinstance(sql, str)
    assert params == []  # Confirming that it returns the correct output format without errors