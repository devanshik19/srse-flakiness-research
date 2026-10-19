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

class TestBaseConstraint:
    @pytest.fixture
    def constraint(self):
        class DummyConstraint(BaseConstraint):
            def __init__(self, name, violation_error_message=None):
                self.name = name
                self.violation_error_message = violation_error_message
                self.default_violation_error_message = "Default Error"

        return DummyConstraint(name="test_constraint", violation_error_message="Custom Error")

    def test_deconstruct_with_custom_violation_error_message(self, constraint):
        path, args, kwargs = constraint.deconstruct()
        assert path == "django.db.models.DummyConstraint"
        assert kwargs == {"name": "test_constraint", "violation_error_message": "Custom Error"}

    def test_deconstruct_with_default_violation_error_message(self, constraint):
        constraint.violation_error_message = None
        path, args, kwargs = constraint.deconstruct()
        assert path == "django.db.models.DummyConstraint"
        assert kwargs == {"name": "test_constraint"}