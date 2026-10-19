import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict

@pytest.mark.django_db
def test_model_to_dict_all_fields():
    user = User.objects.create(username="testuser", email="test@example.com", password="securepassword")
    expected_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': '',
        'last_name': '',
        'is_active': True,
        'is_staff': False,
        'is_superuser': False,
        'last_login': None,
        'date_joined': user.date_joined,
    }
    data = model_to_dict(user)
    assert data == expected_data

def test_model_to_dict_with_fields():
    user = User.objects.create(username="testuser2", email="test2@example.com")
    data = model_to_dict(user, fields=['username', 'email'])
    assert data == {
        'username': user.username,
        'email': user.email,
    }

def test_model_to_dict_with_exclude():
    user = User.objects.create(username="testuser3", email="test3@example.com")
    data = model_to_dict(user, exclude=['username'])
    assert 'username' not in data

def test_model_to_dict_with_fields_and_exclude():
    user = User.objects.create(username="testuser4", email="test4@example.com", first_name="Test")
    data = model_to_dict(user, fields=['username', 'first_name', 'email'], exclude=['email'])
    assert data == {
        'username': user.username,
        'first_name': user.first_name,
    }

def test_model_to_dict_no_editable_fields():
    class NonEditableModel:
        _meta = type('Meta', (object,), {
            'concrete_fields': [],
            'private_fields': [],
            'many_to_many': [],
        })()
    
    instance = NonEditableModel()
    data = model_to_dict(instance)
    assert data == {}