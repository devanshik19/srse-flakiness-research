import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict

def test_model_to_dict_with_all_fields():
    user = User.objects.create(username='testuser', password='testpassword', email='test@example.com')
    result = model_to_dict(user)
    assert result['username'] == 'testuser'
    assert result['email'] == 'test@example.com'

def test_model_to_dict_with_fields():
    user = User.objects.create(username='testuser', password='testpassword', email='test@example.com')
    result = model_to_dict(user, fields=['username', 'email'])
    assert result == {'username': 'testuser', 'email': 'test@example.com'}

def test_model_to_dict_with_exclude():
    user = User.objects.create(username='testuser', password='testpassword', email='test@example.com')
    result = model_to_dict(user, exclude=['email'])
    assert 'email' not in result
    assert result['username'] == 'testuser'

def test_model_to_dict_with_fields_and_exclude():
    user = User.objects.create(username='testuser', password='testpassword', email='test@example.com')
    result = model_to_dict(user, fields=['username', 'email'], exclude=['username'])
    assert 'username' not in result
    assert result['email'] == 'test@example.com'

def test_model_to_dict_with_no_editable_fields():
    # Assuming a custom model where we manipulate 'editable' can be difficult,
    # for this example, we rely on User's default fields for testing.
    user = User.objects.create(username='testuser', password='testpassword', email='test@example.com')
    with pytest.raises(ValidationError):
        model_to_dict(user, fields=['is_active'])  # `is_active` is not a required field
        
    # Ensure that only editable fields are returned
    result = model_to_dict(user, fields=['username', 'is_staff'])
    assert result['username'] == 'testuser'