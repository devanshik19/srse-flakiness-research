import warnings
import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import DEFAULT_DB_ALIAS
from django.db.models.constraints import BaseConstraint

class TestBaseConstraint(BaseConstraint):
    def validate(self, model, instance, exclude=None, using=DEFAULT_DB_ALIAS):
        raise ValidationError("Validation failed.")

def test_validate_raises_not_implemented_error():
    constraint = BaseConstraint()
    with pytest.raises(NotImplementedError, match="must be implemented by a subclass"):
        constraint.validate(User, User())

def test_validate_raises_validation_error():
    constraint = TestBaseConstraint()
    with pytest.raises(ValidationError, match="Validation failed."):
        constraint.validate(User, User())