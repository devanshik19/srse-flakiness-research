import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.forms import ModelForm
from django.forms.models import modelform_factory

# Test cases for the modelform_factory function
def test_modelform_factory_with_fields():
    # Create a form class for the User model specifying fields
    UserForm = modelform_factory(User, fields=('username', 'password'))
    user_data = {'username': 'testuser', 'password': 'testpassword'}
    
    form = UserForm(data=user_data)
    assert form.is_valid()  # Check if the form is valid
    user = form.save()  # Save the instance
    assert user.username == 'testuser'  # Check if the username is set correctly

def test_modelform_factory_with_exclude():
    # Create a form class for the User model excluding 'password'
    UserForm = modelform_factory(User, exclude=('password',))
    user_data = {'username': 'testuser'}
    
    form = UserForm(data=user_data)
    assert form.is_valid()  # Check if the form is valid
    user = form.save()  # Save the instance
    assert user.username == 'testuser'  # Check if the username is set correctly

def test_modelform_factory_without_fields_or_exclude():
    with pytest.raises(ImproperlyConfigured) as excinfo:
        modelform_factory(User)
    assert str(excinfo.value) == (
        "Calling modelform_factory without defining 'fields' or "
        "'exclude' explicitly is prohibited."
    )

def test_modelform_factory_with_widgets():
    # Create a form class with a specific widget for 'username'
    from django.forms.widgets import TextInput
    UserForm = modelform_factory(User, widgets={'username': TextInput(attrs={'class': 'username'})})
    assert 'username' in UserForm.base_fields  # Check if username field exists
    assert isinstance(UserForm.base_fields['username'].widget, TextInput)  # Check widget type

def test_modelform_factory_with_labels():
    # Create a form class with specific labels for fields
    UserForm = modelform_factory(User, labels={'username': 'User Name', 'password': 'Password'})
    assert UserForm.base_fields['username'].label == 'User Name'  # Check custom label
    assert UserForm.base_fields['password'].label == 'Password'  # Check custom label