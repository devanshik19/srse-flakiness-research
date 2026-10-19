import pytest
from django.contrib.auth.models import User
from django.db.models import Model
from django.core.exceptions import ValidationError
from django.db import DEFAULT_DB_ALIAS

class BaseConstraint:
    default_violation_error_message = "Default error message."
    violation_error_message = "Violation error message."

    def __init__(self):
        pass

    def contains_expressions(self):
        return False

    def constraint_sql(self, model, schema_editor):
        pass

    def create_sql(self, model, schema_editor):
        pass

    def remove_sql(self, model, schema_editor):
        pass

    def validate(self, model, instance, exclude=None, using=DEFAULT_DB_ALIAS):
        raise NotImplementedError("This method must be implemented by a subclass.")

    def get_violation_error_message(self):
        return self.violation_error_message

    def deconstruct(self):
        pass

    def clone(self):
        pass


class TestBaseConstraint:
    @pytest.fixture
    def constraint(self):
        return BaseConstraint()

    def test_validate_not_implemented(self, constraint):
        model = User
        instance = User(username="testuser")

        with pytest.raises(NotImplementedError, match="This method must be implemented by a subclass."):
            constraint.validate(model, instance)

    def test_get_violation_error_message(self, constraint):
        assert constraint.get_violation_error_message() == "Violation error message."