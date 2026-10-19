import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.forms import ModelForm

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField()

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']

def test_inlineformset_factory():
    # Create a parent instance
    user = User.objects.create_user('testuser', 'test@example.com', 'password123')
    
    # Create the inline formset factory
    ProfileFormSet = inlineformset_factory(User, Profile, form=ProfileForm, extra=2)

    # Create an instance of the formset
    formset = ProfileFormSet(instance=user)
    
    # Check the number of forms created
    assert len(formset.forms) == 2  # extra=2
    
    # Check the initial data
    assert formset.initial == []
    
    # Populate the formset with valid data
    valid_data = {
        'form-0-bio': 'Bio 1',
        'form-1-bio': 'Bio 2',
        'form-2-bio': '',  # Should be empty for the extra form
        'form-0-id': '',
        'form-1-id': '',
        'form-2-id': '',
        'form-TOTAL_FORMS': '3',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': '',
    }
    
    formset = ProfileFormSet(data=valid_data, instance=user)
    
    # Validate the formset
    assert formset.is_valid() is True
    
    # Save the formset
    formset.save()
    
    # Verify the created profiles
    assert Profile.objects.count() == 2
    assert Profile.objects.filter(user=user, bio='Bio 1').exists()
    assert Profile.objects.filter(user=user, bio='Bio 2').exists()