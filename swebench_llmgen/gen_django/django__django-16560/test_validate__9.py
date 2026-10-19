import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import DEFAULT_DB_ALIAS
from django.db.models.constraints import BaseConstraint

class ConcreteConstraint(BaseConstraint):
    def validate(self, model, instance, exclude=None, using=DEFAULT_DB_ALIAS):
        if not isinstance(instance, model):
            raise ValidationError("Instance does not match the model.")
        
        if instance.username == "":
            raise ValidationError("Username cannot be empty.")

@pytest.fixture
def user_instance():
    return User(username="testuser")

def test_validate_correct_instance(user_instance):
    constraint = ConcreteConstraint()
    try:
        constraint.validate(User, user_instance)
    except ValidationError:
        pytest.fail("Validation raised an unexpected ValidationError.")

def test_validate_incorrect_instance():
    constraint = ConcreteConstraint()
    wrong_instance = "not_a_user_instance"
    
    with pytest.raises(ValidationError, match="Instance does not match the model."):
        constraint.validate(User, wrong_instance)

def test_validate_empty_username(user_instance):
    user_instance.username = ""
    constraint = ConcreteConstraint()
    
    with pytest.raises(ValidationError, match="Username cannot be empty."):
        constraint.validate(User, user_instance)