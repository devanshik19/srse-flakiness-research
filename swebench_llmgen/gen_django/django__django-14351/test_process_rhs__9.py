import itertools
import math
from copy import copy
from django.core.exceptions import EmptyResultSet
from django.db.models.expressions import Case, Func, Value, When
from django.db.models.fields import CharField, DateTimeField, Field, IntegerField, UUIDField
from django.db.models.query_utils import RegisterLookupMixin
from django.utils.datastructures import OrderedSet
from django.utils.functional import cached_property
from django.utils.hashable import make_hashable
from django.contrib.auth.models import User
from django.db.models import Q


class TestLookup:

    def test_process_rhs_direct_value(self, compiler, connection):
        lookup = Lookup(lhs=User.username, rhs='test_user')
        lookup.bilateral_transforms = False  # Simulate no transforms
        
        sql, params = lookup.process_rhs(compiler, connection)
        
        assert sql == "(username = %s)"
        assert params == ['test_user']

    def test_process_rhs_bilateral_transforms(self, compiler, connection):
        lookup = Lookup(lhs=User.username, rhs='test_user')
        lookup.bilateral_transforms = True  # Simulate bilateral transforms
        
        def mock_apply_bilateral_transforms(value):
            return Value(value + "_transformed")
        
        def mock_rhs_is_direct_value():
            return True
        
        lookup.apply_bilateral_transforms = mock_apply_bilateral_transforms
        lookup.rhs_is_direct_value = mock_rhs_is_direct_value
        
        sql, params = lookup.process_rhs(compiler, connection)
        
        assert sql == "(username = %s)"
        assert params == ['test_user_transformed']

    def test_process_rhs_expression(self, compiler, connection):
        lookup = Lookup(lhs=User.username, rhs=Value('example_user'))
        lookup.bilateral_transforms = False
        
        sql, params = lookup.process_rhs(compiler, connection)
        
        assert sql.startswith("(")
        assert sql.endswith(")")
        assert params == ['example_user']

    def test_process_rhs_get_db_prep_lookup(self, compiler, connection):
        lookup = Lookup(lhs=User.username, rhs='test_user')
        lookup.bilateral_transforms = False
        
        def mock_get_db_prep_lookup(value, connection):
            return 'Prepared SQL', ['prepared_param']
        
        lookup.get_db_prep_lookup = mock_get_db_prep_lookup
        
        sql, params = lookup.process_rhs(compiler, connection)
        
        assert sql == 'Prepared SQL'
        assert params == ['prepared_param']