import itertools
import math
from copy import copy
from django.core.exceptions import EmptyResultSet
from django.db.models.expressions import Case, Func, Value, When
from django.db.models.fields import (
    CharField, DateTimeField, Field, IntegerField, UUIDField,
)
from django.db.models.query_utils import RegisterLookupMixin
from django.utils.datastructures import OrderedSet
from django.utils.functional import cached_property
from django.utils.hashable import make_hashable

import pytest
from django.contrib.auth.models import User
from django.db.models import Lookup

class CustomLookup(Lookup):
    def rhs_is_direct_value(self):
        return isinstance(self.rhs, (str, int, float, bool))

    def apply_bilateral_transforms(self, value):
        # Example transformation; simply return the value
        return value

    def get_db_prep_lookup(self, value, connection):
        # Dummy implementation for testing
        return (f"DB prepared value: {value}", [])

@pytest.fixture
def user_lookup():
    user = User(username='testuser', password='password')
    user.save()
    yield CustomLookup(lhs=CharField(), rhs='test_value')

def test_process_rhs_with_direct_value(user_lookup):
    user_lookup.lookup_name = 'test_lookup'
    user_lookup.bilateral_transforms = True

    compiler = None  # Use an appropriate compiler mock if needed
    connection = None  # Use an appropriate connection mock if needed

    sql, params = user_lookup.process_rhs(compiler, connection)
    assert sql == '(DB prepared value: test_value)'
    assert params == []

def test_process_rhs_with_non_direct_value(user_lookup):
    user_lookup.rhs = Func(Value('non_direct_value'))
    user_lookup.bilateral_transforms = False

    compiler = None  # Use an appropriate compiler mock if needed
    connection = None  # Use an appropriate connection mock if needed

    sql, params = user_lookup.process_rhs(compiler, connection)
    assert sql.startswith('(') and sql.endswith(')')  # Check parentheses
    assert params == []  # Adjust as necessary based on your implementation

def test_process_rhs_without_bilateral_transforms(user_lookup):
    user_lookup.bilateral_transforms = False
    user_lookup.rhs = Value('no_transform')

    compiler = None  # Use an appropriate compiler mock if needed
    connection = None  # Use an appropriate connection mock if needed

    sql, params = user_lookup.process_rhs(compiler, connection)
    assert sql == 'DB prepared value: no_transform'
    assert params == []