import pytest
from django import forms
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.forms import ModelForm

# Define a simple model for testing: 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']

@pytest.mark.parametrize("fk_name, expected_max_num", [(None, 3), ('user', 1)])
def test_inlineformset_factory(fk_name, expected_max_num):
    # given
    user = User.objects.create(username='testuser')
    profile_formset = inlineformset_factory(User, Profile, form=ProfileForm, fk_name=fk_name)

    # when
    formset = profile_formset(instance=user)

    # then
    assert formset.extra == expected_max_num
    
    # test adding profiles through formset
    formset_data = {'bio': ['Bio 1', 'Bio 2', 'Bio 3', 'Bio 4']}
    formset = profile_formset(data={'form-0-bio': 'Bio 1', 'form-1-bio': 'Bio 2',
                                      'form-2-bio': 'Bio 3', 'form-TOTAL_FORMS': 3})

    assert formset.is_valid()
    formset.save()

    # validate the profiles were created
    assert Profile.objects.count() == 3
    assert Profile.objects.filter(bio='Bio 1').exists()
    assert Profile.objects.filter(bio='Bio 2').exists()
    assert Profile.objects.filter(bio='Bio 3').exists()