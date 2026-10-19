import pytest
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']


def test_inlineformset_factory():
    # Create a user instance
    user = User.objects.create_user(username='testuser', password='password')

    # Create InlineFormSet for Profile model
    ProfileFormSet = inlineformset_factory(User, Profile, form=ProfileForm, extra=2)

    # Create an instance of the formset with the user instance
    formset = ProfileFormSet(instance=user)

    # Check the initial number of forms is the extra number specified
    assert len(formset) == 2

    # Fill the formset with data
    formset_data = {
        'profile_set-0-bio': 'Bio 1',
        'profile_set-1-bio': 'Bio 2',
        'profile_set-TOTAL_FORMS': 2,
        'profile_set-INITIAL_FORMS': 0,
        'profile_set-MAX_NUM_FORMS': ''
    }

    formset = ProfileFormSet(data=formset_data, instance=user)

    # Formset should be valid
    assert formset.is_valid()

    # Save the formset and check if objects are created
    formset.save()
    assert Profile.objects.count() == 2

    # Clean up
    user.delete()