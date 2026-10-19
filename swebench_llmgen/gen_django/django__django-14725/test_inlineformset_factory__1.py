import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.forms import ModelForm, BaseFormSet


# Creating a simple model for test purpose
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField()


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']


def test_inlineformset_factory():
    # Create a user instance
    user_instance = User.objects.create(username='testuser')

    # Creating an inline formset factory
    ProfileInlineFormSet = inlineformset_factory(
        User,
        Profile,
        form=ProfileForm,
        extra=2,
        can_delete=True
    )

    # Creating an inline formset instance for the user
    formset = ProfileInlineFormSet(instance=user_instance)

    # Check initial formset is as expected with extra empty forms
    assert len(formset) == 2
    assert all(isinstance(form, ProfileForm) for form in formset)

    # Simulating form submission with valid data
    formset_data = {
        'form-0-bio': 'Bio for first profile',
        'form-1-bio': 'Bio for second profile',
        'form-0-id': '',  # No id means new profile
        'form-1-id': '',  # No id means new profile
        'form-0-DELETE': 'False',
        'form-1-DELETE': 'False',
    }
    formset = ProfileInlineFormSet(data=formset_data, instance=user_instance)

    # Check if formset is valid
    assert formset.is_valid()

    # Save the formset
    formset.save()

    # Verify that the profiles were created
    assert Profile.objects.count() == 2
    assert Profile.objects.filter(user=user_instance).count() == 2
    assert Profile.objects.first().bio == 'Bio for first profile'
    assert Profile.objects.last().bio == 'Bio for second profile'