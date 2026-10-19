import pytest
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class UserCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Confirm password"), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username",)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

@pytest.mark.django_db
def test_user_creation_form_save():
    form_data = {
        'username': 'testuser',
        'password1': 'testpassword',
        'password2': 'testpassword',
    }
    form = UserCreationForm(data=form_data)
    assert form.is_valid()
    
    user = form.save()
    assert user.username == 'testuser'
    assert user.check_password('testpassword') is True

    # Test with different passwords
    form_data_mismatch = {
        'username': 'testuser2',
        'password1': 'testpassword',
        'password2': 'differentpassword',
    }
    form_mismatch = UserCreationForm(data=form_data_mismatch)
    assert not form_mismatch.is_valid()
    assert 'password_mismatch' in form_mismatch.errors['password2']