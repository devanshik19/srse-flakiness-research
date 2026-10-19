import pytest
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

def test_model_to_dict_with_all_fields():
    user = User.objects.create(username='testuser', email='test@example.com', password='password')
    expected_data = {
        'id': user.id,
        'username': 'testuser',
        'email': 'test@example.com',
    }
    result = model_to_dict(user)
    assert result == expected_data

def test_model_to_dict_with_specific_fields():
    user = User.objects.create(username='testuser', email='test@example.com', password='password')
    expected_data = {
        'username': 'testuser',
        'email': 'test@example.com',
    }
    result = model_to_dict(user, fields=['username', 'email'])
    assert result == expected_data

def test_model_to_dict_with_excluded_fields():
    user = User.objects.create(username='testuser', email='test@example.com', password='password')
    expected_data = {
        'username': 'testuser',
    }
    result = model_to_dict(user, exclude=['email'])
    assert result == expected_data

def test_model_to_dict_with_fields_and_exclusions():
    user = User.objects.create(username='testuser', email='test@example.com', password='password')
    expected_data = {
        'username': 'testuser',
    }
    result = model_to_dict(user, fields=['username', 'email'], exclude=['email'])
    assert result == expected_data

def test_model_to_dict_with_no_editable_fields():
    class NonEditableUser(User):
        class Meta:
            model = User
            fields = ('username',)  # Simulating a model with non-editable fields
            editable = False

    non_editable_user = NonEditableUser(username='testuser')
    expected_data = {}
    result = model_to_dict(non_editable_user)
    assert result == expected_data