import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import DEFAULT_DB_ALIAS


class TestBaseConstraint:

    class ConcreteConstraint(BaseConstraint):
        def validate(self, model, instance, exclude=None, using=DEFAULT_DB_ALIAS):
            if not isinstance(instance, model):
                raise ValidationError("Invalid model instance.")

    @pytest.fixture
    def user_instance(self):
        return User(username='testuser', password='testpass')

    def test_validate_success(self, user_instance):
        constraint = self.ConcreteConstraint()
        try:
            constraint.validate(User, user_instance)
        except ValidationError:
            pytest.fail("Validation should not raise an error for a valid instance.")

    def test_validate_failure_invalid_instance(self, user_instance):
        class AnotherModel:
            pass
        
        constraint = self.ConcreteConstraint()
        
        with pytest.raises(ValidationError, match="Invalid model instance."):
            constraint.validate(User, AnotherModel())