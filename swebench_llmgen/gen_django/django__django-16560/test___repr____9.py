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
from django.db.models import CheckConstraint, Q
from django.contrib.auth.models import User

def test_check_constraint_repr():
    # Setup
    check = CheckConstraint(check=Q(username__isnull=False), name='check_username_not_null', violation_error_message='Username cannot be null')

    # Test __repr__ with all fields
    assert repr(check) == "<CheckConstraint: check=Q(username__isnull=False) name='check_username_not_null' violation_error_message='Username cannot be null'>"
    
    # Test __repr__ with default violation_error_message
    check_default_error = CheckConstraint(check=Q(username__isnull=False), name='check_username_not_null')
    assert repr(check_default_error) == "<CheckConstraint: check=Q(username__isnull=False) name='check_username_not_null'>"

    # Test __repr__ with NoneType violation_error_message
    check_none_error = CheckConstraint(check=Q(username__isnull=False), name='check_username_not_null', violation_error_message=None)
    assert repr(check_none_error) == "<CheckConstraint: check=Q(username__isnull=False) name='check_username_not_null'>"