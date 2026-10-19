import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.forms import ModelForm, BaseInlineFormSet

# Create a simple model for testing
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField()

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']

# Test inlineformset_factory
def test_inlineformset_factory():
    # Arrange
    user = User.objects.create(username='testuser')
    InlineFormSet = inlineformset_factory(User, Profile, form=ProfileForm, extra=2, can_delete=True)

    # Act
    formset = InlineFormSet(instance=user)

    # Assert
    assert formset.extra == 2
    assert hasattr(formset, 'fk')
    assert formset.fk == 'user'
    assert isinstance(formset, BaseInlineFormSet)

    # Test validation and formset length
    formset_data = {
        'form-0-bio': 'Bio 1',
        'form-1-bio': '',  # Invalid data, empty bio
        'form-2-bio': 'Bio 3',
        'form-0-DELETE': 'on',
    }
    formset = InlineFormSet(data=formset_data, instance=user)

    # Check if formset is valid
    assert not formset.is_valid()
    assert len(formset.errors) == 1  # There should be error for the second form
    assert formset.total_form_count() == 3  # 2 extra forms + 1 must be present

    # Simulate valid data for saving
    formset_data_valid = {
        'form-0-bio': 'Bio 1',
        'form-1-bio': 'Bio 2',
        'form-0-DELETE': 'on',  # Delete first profile
    }
    formset = InlineFormSet(data=formset_data_valid, instance=user)

    # Check if formset is valid after modification
    assert formset.is_valid()

    # Save the formset
    formset.save()
    
    # Assert that profiles saved correctly
    assert Profile.objects.count() == 1
    assert Profile.objects.filter(user=user).first().bio == 'Bio 2'