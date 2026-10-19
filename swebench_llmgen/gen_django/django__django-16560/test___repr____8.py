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
    # Test with default violation_error_message
    check = CheckConstraint(check="some_check", name="test_constraint")
    expected_repr = "<CheckConstraint: check=some_check name='test_constraint'>"
    assert repr(check) == expected_repr

    # Test with custom violation_error_message
    check.violation_error_message = "Custom violation message"
    expected_repr_custom_message = "<CheckConstraint: check=some_check name='test_constraint' violation_error_message='Custom violation message'>"
    assert repr(check) == expected_repr_custom_message

    # Test with None violation_error_message
    check.violation_error_message = None
    expected_repr_none_message = "<CheckConstraint: check=some_check name='test_constraint'>"
    assert repr(check) == expected_repr_none_message

    # Test with another default message
    check.default_violation_error_message = "Default error message"
    check.violation_error_message = "Default error message"
    assert repr(check) == expected_repr