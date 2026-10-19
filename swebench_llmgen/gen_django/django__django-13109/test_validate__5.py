import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

class ForeignKey(models.ForeignKey):
    def validate(self, value, model_instance):
        if self.remote_field.parent_link:
            return
        super().validate(value, model_instance)
        if value is None:
            return

        using = router.db_for_read(self.remote_field.model, instance=model_instance)
        qs = self.remote_field.model._default_manager.using(using).filter(
            **{self.remote_field.field_name: value}
        )
        qs = qs.complex_filter(self.get_limit_choices_to())
        if not qs.exists():
            raise ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={
                    'model': self.remote_field.model._meta.verbose_name, 
                    'pk': value,
                    'field': self.remote_field.field_name, 
                    'value': value,
                },
            )

class TestForeignKeyValidation:
    @pytest.fixture
    def user(self):
        return User.objects.create(username='testuser')

    @pytest.fixture
    def foreign_key(self, user):
        class ExampleModel(models.Model):
            user = ForeignKey(User, on_delete=models.CASCADE)

        yield ExampleModel._meta.get_field('user')

    def test_validate_success(self, foreign_key, user):
        foreign_key.validate(user.id, None)  # Should not raise an error

    def test_validate_none(self, foreign_key):
        foreign_key.validate(None, None)  # Should not raise an error

    def test_validate_invalid(self, foreign_key):
        with pytest.raises(ValidationError):
            foreign_key.validate(999, None)  # No such user with id 999