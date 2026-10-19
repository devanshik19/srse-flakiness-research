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
    password2 = forms.CharField(label=_("Confirm Password"), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',)

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

def test_user_creation_form_save():
    form_data = {
        'username': 'testuser',
        'password1': 'securepassword123',
        'password2': 'securepassword123',
    }
    form = UserCreationForm(data=form_data)

    assert form.is_valid(), form.errors
    user = form.save()
    
    assert user.username == 'testuser'
    assert user.check_password('securepassword123')
    
    # Test the user is saved in the database
    assert User.objects.filter(username='testuser').exists()

def test_user_creation_form_save_password_mismatch():
    form_data = {
        'username': 'testuser2',
        'password1': 'securepassword123',
        'password2': 'differentpassword456',
    }
    form = UserCreationForm(data=form_data)

    assert not form.is_valid()
    assert 'password_mismatch' in form.errors['password2']