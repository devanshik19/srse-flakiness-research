import pytest
from django.contrib.auth.models import User
from django.core import exceptions
from django.db import models

class ForeignKey:
    def __init__(self, to, on_delete, related_name=None, related_query_name=None, limit_choices_to=None, parent_link=False):
        self.remote_field = self
        self.model = to
        self.on_delete = on_delete
        self.field_name = 'id'
        self.parent_link = parent_link
        self.error_messages = {'invalid': 'Invalid value for {field}.'}

    def validate(self, value, model_instance):
        if self.remote_field.parent_link:
            return
        if value is None:
            return
        
        using = 'default'  # Simplified for testing
        qs = self.remote_field.model._default_manager.filter(**{self.field_name: value})
        if not qs.exists():
            raise exceptions.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={
                    'model': self.remote_field.model._meta.verbose_name, 'pk': value,
                    'field': self.field_name, 'value': value,
                },
            )
            
@pytest.mark.django_db
def test_foreign_key_validate_correct_value():
    user = User.objects.create(username='testuser')
    fk = ForeignKey(to=User, on_delete=models.CASCADE)

    # Test with valid value
    fk.validate(user.pk, model_instance=None)

@pytest.mark.django_db
def test_foreign_key_validate_none_value():
    fk = ForeignKey(to=User, on_delete=models.CASCADE)

    # Test with None value
    fk.validate(None, model_instance=None)

@pytest.mark.django_db
def test_foreign_key_validate_invalid_value():
    fk = ForeignKey(to=User, on_delete=models.CASCADE)

    # Test with an invalid value and check for ValidationError
    with pytest.raises(exceptions.ValidationError) as excinfo:
        fk.validate(9999, model_instance=None)
    
    assert str(excinfo.value) == 'Invalid value for id.'