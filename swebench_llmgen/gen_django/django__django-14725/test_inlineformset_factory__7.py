import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.forms.models import BaseInlineFormSet

# Test models related to User for testing inlineformset_factory
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField()

# Test function to check the behavior of inlineformset_factory
def test_inlineformset_factory():
    # Create a user instance
    user = User.objects.create_user(username='testuser', password='testpassword')
    
    # Create an inline formset for the Profile model
    ProfileFormSet = inlineformset_factory(User, Profile, fields=('bio',), extra=2)

    # Checking if the formset is correctly initialized
    formset = ProfileFormSet(instance=user)
    assert formset.is_valid() is True
    assert len(formset.forms) == 2  # Checking that we have two forms as defined by 'extra=2'

    # Testing formset with valid data
    data = {
        '0-bio': 'This is a bio for profile 1',
        '1-bio': 'This is a bio for profile 2',
    }
    formset = ProfileFormSet(data=data, instance=user)
    assert formset.is_valid() is True
    
    # Save the formset
    formset.save()
    assert Profile.objects.count() == 2  # Ensuring two profiles were created for the user

    # Testing with invalid data
    data_invalid = {
        '0-bio': '',
        '1-bio': 'This is a bio for profile 2',
    }
    formset_invalid = ProfileFormSet(data=data_invalid, instance=user)
    assert formset_invalid.is_valid() is False
    assert 'bio' in formset_invalid.errors[0]  # Checking for the correct error

    # Testing max_num limitation
    ProfileFormSetMax = inlineformset_factory(User, Profile, fields=('bio',), extra=2, max_num=1)
    formset_max = ProfileFormSetMax(instance=user)
    assert formset_max.is_valid() is True
    assert len(formset_max.forms) == 1  # Should only produce one form due to max_num=1