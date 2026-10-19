import copy
import datetime
from decimal import Decimal
from django.core.exceptions import FieldError
from django.db import connection
from django.db.models import DurationField
from django.db.models.expressions import DurationExpression
from django.db.models.sql.compiler import SQLCompiler
from django.contrib.auth.models import User

class TestDurationExpression:

    def test_compile_duration_field(self):
        # Setup
        user = User.objects.create(username='testuser', password='password')
        duration_field = DurationField()
        
        # Create a mock side with the expected output_field
        class MockSide:
            output_field = duration_field
        
        # Create a mock compiler
        class MockCompiler(SQLCompiler):
            def compile(self, side):
                return 'SELECT * FROM auth_user', []

        duration_expr = DurationExpression()
        compiler = MockCompiler()

        # Act
        sql, params = duration_expr.compile(MockSide(), compiler, connection)

        # Assert
        assert sql == 'SELECT * FROM auth_user'
        assert params == []

    def test_compile_field_error(self):
        # Setup
        user = User.objects.create(username='testuser', password='password')
        
        # Create a mock side with a missing output_field
        class MockSide:
            output_field = None
        
        # Create a mock compiler
        class MockCompiler(SQLCompiler):
            def compile(self, side):
                return 'SELECT id FROM auth_user', []

        duration_expr = DurationExpression()
        compiler = MockCompiler()

        # Act
        sql, params = duration_expr.compile(MockSide(), compiler, connection)

        # Assert
        assert sql == 'SELECT id FROM auth_user'
        assert params == []