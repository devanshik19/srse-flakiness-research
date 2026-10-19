import copy
import datetime
import inspect
from decimal import Decimal
from django.core.exceptions import EmptyResultSet, FieldError
from django.db import NotSupportedError, connection
from django.db.models import fields
from django.db.models.constants import LOOKUP_SEP
from django.db.models.query_utils import Q
from django.utils.deconstruct import deconstructible
from django.utils.functional import cached_property
from django.utils.hashable import make_hashable
from django.contrib.auth.models import User
from django.db import models

class DurationField(models.DurationField):
    def db_type(self, connection):
        return 'interval'

class MockCompiler:
    def compile(self, expression):
        return 'SELECT * FROM my_table', []

class MockSide:
    def __init__(self, output_field):
        self.output_field = output_field

def test_compile_duration_field():
    duration_expression = DurationExpression()
    compiler = MockCompiler()
    
    # Test case where output_field is a DurationField
    mock_duration_field = DurationField()
    side_with_duration = MockSide(mock_duration_field)
    sql, params = duration_expression.compile(side_with_duration, compiler, connection)
    
    assert sql == 'SELECT * FROM my_table'
    assert params == []
    
def test_compile_non_duration_field():
    duration_expression = DurationExpression()
    compiler = MockCompiler()
    
    # Test case where output_field is not a DurationField
    mock_non_duration_field = fields.IntegerField()
    side_with_non_duration = MockSide(mock_non_duration_field)
    sql, params = duration_expression.compile(side_with_non_duration, compiler, connection)
    
    assert sql == 'SELECT * FROM my_table'
    assert params == []
    
def test_compile_field_error():
    duration_expression = DurationExpression()
    compiler = MockCompiler()
    
    # Test case where accessing output_field raises FieldError
    class SideWithFieldError:
        @property
        def output_field(self):
            raise FieldError("Field does not exist")
    
    side_with_error = SideWithFieldError()
    sql, params = duration_expression.compile(side_with_error, compiler, connection)
    
    assert sql == 'SELECT * FROM my_table'
    assert params == []