import pytest
from django.contrib.auth.models import User
from django.core import exceptions
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
            raise exceptions.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={
                    'model': self.remote_field.model._meta.verbose_name,
                    'pk': value,
                    'field': self.remote_field.field_name,
                    'value': value,
                },
            )

@pytest.mark.django_db
def test_foreign_key_validate_existing_object():
    user = User.objects.create(username='testuser', password='password')
    foreign_key_field = ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='related_users'
    )
    
    # Valid case, existing User
    try:
        foreign_key_field.validate(user.id, None)
    except exceptions.ValidationError:
        pytest.fail("Validation raised an error for an existing object.")

@pytest.mark.django_db
def test_foreign_key_validate_non_existing_object():
    foreign_key_field = ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='related_users'
    )
    
    # Invalid case, non-existing User
    with pytest.raises(exceptions.ValidationError) as excinfo:
        foreign_key_field.validate(99999, None)
    assert excinfo.value.code == 'invalid'

@pytest.mark.django_db
def test_foreign_key_validate_none_value():
    foreign_key_field = ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='related_users'
    )
    
    # Valid case, value is None
    foreign_key_field.validate(None, None)  # Should not raise any exception