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
from django.db.models import Model
from django.contrib.auth.models import User

class CheckConstraint:
    def __init__(self, check, name, violation_error_message=None):
        self.check = check
        self.name = name
        self.violation_error_message = violation_error_message
        self.default_violation_error_message = "A check constraint is violated."

    def __repr__(self):
        return "<%s: check=%s name=%s%s>" % (
            self.__class__.__qualname__,
            self.check,
            repr(self.name),
            (
                ""
                if self.violation_error_message is None
                or self.violation_error_message == self.default_violation_error_message
                else " violation_error_message=%r" % self.violation_error_message
            ),
        )

def test_check_constraint_repr_default_message():
    constraint = CheckConstraint(check='age > 18', name='age_check')
    expected_repr = "<CheckConstraint: check=age > 18 name='age_check'>"
    assert repr(constraint) == expected_repr

def test_check_constraint_repr_custom_message():
    constraint = CheckConstraint(check='age > 18', name='age_check', violation_error_message='Age must be above 18')
    expected_repr = "<CheckConstraint: check=age > 18 name='age_check' violation_error_message='Age must be above 18'>"
    assert repr(constraint) == expected_repr

def test_check_constraint_repr_no_violation_message():
    constraint = CheckConstraint(check='age > 18', name='age_check', violation_error_message=None)
    expected_repr = "<CheckConstraint: check=age > 18 name='age_check'>"
    assert repr(constraint) == expected_repr