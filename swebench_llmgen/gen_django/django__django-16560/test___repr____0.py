import warnings
from enum import Enum
from types import NoneType
from django.core.exceptions import FieldError, ValidationError
from django.db import connections
from django.db.models.expressions import Exists, ExpressionList, F, OrderBy
from django.db.models.indexes import IndexExpression
from django.db.models.lookups import Exact
from django.db.models.query_utils import Q
from django.db.models.sql.query import Query
from django.db.utils import DEFAULT_DB_ALIAS
from django.utils.deprecation import RemovedInDjango60Warning
from django.utils.translation import gettext_lazy as _
from django.db.models import CheckConstraint

def test_check_constraint_repr():
    # Test 1: Default violation error message
    constraint = CheckConstraint(check=Q(username__isnull=False), name='username_not_null')
    assert repr(constraint) == "<CheckConstraint: check=<Q: (AND: ('username__isnull', False))> name='username_not_null'>"

    # Test 2: Custom violation error message
    constraint.violation_error_message = "Username cannot be null"
    expected_repr = "<CheckConstraint: check=<Q: (AND: ('username__isnull', False))> name='username_not_null' violation_error_message='Username cannot be null'>"
    assert repr(constraint) == expected_repr

    # Test 3: Missing violation error message
    constraint.violation_error_message = None
    assert repr(constraint) == "<CheckConstraint: check=<Q: (AND: ('username__isnull', False))> name='username_not_null'>"