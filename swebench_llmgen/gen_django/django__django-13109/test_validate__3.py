import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import ForeignKey

# Extending the ForeignKey class for testing purposes
class TestForeignKey(ForeignKey):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.remote_field = self.remote_field  # Use existing remote_field

    # A simplified version of get_limit_choices_to for testing
    def get_limit_choices_to(self):
        return Q()

# Test case for the validate function
def test_foreign_key_validate():
    # Prepare the ForeignKey with User as the model
    user_fk = TestForeignKey(to=User, on_delete=models.CASCADE)

    # Creating a valid user instance
    user = User.objects.create(username='testuser')

    # Validating existing user
    try:
        user_fk.validate(user.id, None)  # No model_instance needed
    except ValidationError:
        pytest.fail("Validation raised an unexpected ValidationError for existing user.")

    # Validating non-existing user
    with pytest.raises(ValidationError) as excinfo:
        user_fk.validate(999, None)  # Non-existing user ID
    assert excinfo.value.code == 'invalid'
    assert 'model' in excinfo.value.params
    assert excinfo.value.params['model'] == User._meta.verbose_name
    assert excinfo.value.params['pk'] == 999
    assert excinfo.value.params['field'] == user_fk.remote_field.field_name
    assert excinfo.value.params['value'] == 999

    # Validating None value
    user_fk.validate(None, None)  # Should not raise ValidationError