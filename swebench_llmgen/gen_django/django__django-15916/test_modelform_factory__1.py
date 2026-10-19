import pytest
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.core.exceptions import ImproperlyConfigured
from django.forms.models import modelform_factory

@pytest.mark.parametrize("fields, exclude, expected_field_count", [
    (None, None, 7),  # Default User model fields
    (['username', 'email'], None, 2),  # Only username and email
    (None, ['password'], 6),  # Exclude password
    (['username', 'email'], ['email'], 1)  # Only username, exclude email
])
def test_modelform_factory(fields, exclude, expected_field_count):
    UserForm = modelform_factory(User, fields=fields, exclude=exclude)
    form = UserForm()
    assert len(form.fields) == expected_field_count

def test_modelform_factory_improperly_configured():
    with pytest.raises(ImproperlyConfigured):
        modelform_factory(User, fields=None, exclude=None)