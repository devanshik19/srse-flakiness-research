import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import ForeignKey

class TestForeignKeyValidation(ForeignKey):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# Create a simple model to test against
class SampleModel(models.Model):
    user = TestForeignKey(User, on_delete=models.CASCADE)

@pytest.mark.django_db
def test_validate_with_none_value():
    """Test validating with a None value."""
    sample_instance = SampleModel()
    test_fk = SampleModel._meta.get_field('user')
    try:
        test_fk.validate(None, sample_instance)
    except ValidationError:
        pytest.fail("ValidationError raised unexpectedly when validating None")

@pytest.mark.django_db
def test_validate_with_valid_foreign_key():
    """Test validating with a valid User instance."""
    user = User.objects.create(username='testuser')
    sample_instance = SampleModel()
    test_fk = SampleModel._meta.get_field('user')
    try:
        test_fk.validate(user.id, sample_instance)
    except ValidationError:
        pytest.fail("ValidationError raised unexpectedly with a valid foreign key")

@pytest.mark.django_db
def test_validate_with_invalid_foreign_key():
    """Test validating with an invalid User ID."""
    invalid_user_id = 999  # Assuming this ID does not exist
    sample_instance = SampleModel()
    test_fk = SampleModel._meta.get_field('user')
    with pytest.raises(ValidationError) as exc_info:
        test_fk.validate(invalid_user_id, sample_instance)
    assert str(exc_info.value) == test_fk.error_messages['invalid'] % {
        'model': User._meta.verbose_name,
        'pk': invalid_user_id,
        'field': 'user',
        'value': invalid_user_id,
    }