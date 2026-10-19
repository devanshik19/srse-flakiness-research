import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import DEFAULT_DB_ALIAS
from django.db.models.constraints import BaseConstraint

class TestBaseConstraint(BaseConstraint):
    def validate(self, model, instance, exclude=None, using=DEFAULT_DB_ALIAS):
        if not isinstance(instance, model):
            raise ValidationError(f"Instance is not of type {model.__name__}")

def test_validate_with_correct_instance():
    constraint = TestBaseConstraint()
    user = User(username='testuser')
    # This should not raise a ValidationError
    constraint.validate(User, user)

def test_validate_with_incorrect_instance():
    constraint = TestBaseConstraint()
    invalid_instance = "not_a_user"  # This is not a User instance
    with pytest.raises(ValidationError, match="Instance is not of type User"):
        constraint.validate(User, invalid_instance)