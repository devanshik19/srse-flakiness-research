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
from django.contrib.auth.models import User
import pytest

class BaseConstraint:
    def __init__(self, name, violation_error_message=None):
        self.name = name
        self.violation_error_message = violation_error_message
        self.default_violation_error_message = "Default error message"

    def deconstruct(self):
        path = "%s.%s" % (self.__class__.__module__, self.__class__.__name__)
        path = path.replace("django.db.models.constraints", "django.db.models")
        kwargs = {"name": self.name}
        if (
            self.violation_error_message is not None
            and self.violation_error_message != self.default_violation_error_message
        ):
            kwargs["violation_error_message"] = self.violation_error_message
        return (path, (), kwargs)

def test_deconstruct_with_default_message():
    constraint = BaseConstraint(name='my_constraint')
    path, _, kwargs = constraint.deconstruct()
    assert path == 'django.db.models.BaseConstraint'
    assert kwargs == {'name': 'my_constraint'}

def test_deconstruct_with_custom_message():
    constraint = BaseConstraint(name='my_constraint', violation_error_message='Custom error message')
    path, _, kwargs = constraint.deconstruct()
    assert path == 'django.db.models.BaseConstraint'
    assert kwargs == {'name': 'my_constraint', 'violation_error_message': 'Custom error message'}

def test_deconstruct_without_violation_error_message():
    constraint = BaseConstraint(name='test_constraint', violation_error_message=None)
    path, _, kwargs = constraint.deconstruct()
    assert path == 'django.db.models.BaseConstraint'
    assert kwargs == {'name': 'test_constraint'}