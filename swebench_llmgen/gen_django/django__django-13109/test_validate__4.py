import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import ForeignKey
from django.db.models.deletion import CASCADE

# Extending User model to create a model with ForeignKey for testing
class Profile(models.Model):
    user = ForeignKey(User, on_delete=CASCADE)

@pytest.mark.django_db
def test_foreign_key_validate_correct_value():
    user = User.objects.create(username='testuser')
    profile = Profile(user=user)
    profile.full_clean()  # This calls validate under the hood

def test_foreign_key_validate_invalid_value():
    profile = Profile(user=None)
    with pytest.raises(ValidationError):
        profile.full_clean()

def test_foreign_key_validate_non_existent_user():
    profile = Profile(user=999)  # An ID that does not exist
    with pytest.raises(ValidationError) as excinfo:
        profile.full_clean()
    assert 'invalid' in str(excinfo.value)

def test_foreign_key_validate_with_parent_link():
    class RelatedModel(models.Model):
        profile = ForeignKey(Profile, on_delete=CASCADE, related_name='related')

    user = User.objects.create(username='testuser')
    profile = Profile.objects.create(user=user)

    # Simulate the case where remote_field.parent_link is True
    related_model_instance = RelatedModel(profile=profile)
    related_model_instance.full_clean()  # Should not raise