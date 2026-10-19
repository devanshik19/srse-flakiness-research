import pytest
from itertools import chain
from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from django.forms.models import model_to_dict

@pytest.mark.django_db
def test_model_to_dict_with_fields():
    user = User.objects.create_user(username='testuser', password='password123', email='testuser@example.com')
    expected_fields = {'id': user.id, 'username': 'testuser', 'email': 'testuser@example.com'}
    
    result = model_to_dict(user, fields=['id', 'username', 'email'])
    
    assert result == expected_fields

@pytest.mark.django_db
def test_model_to_dict_with_exclude():
    user = User.objects.create_user(username='testuser', password='password123', email='testuser@example.com')
    expected_fields = {'id': user.id, 'username': 'testuser'}
    
    result = model_to_dict(user, exclude=['email'])
    
    assert result == expected_fields

@pytest.mark.django_db
def test_model_to_dict_without_fields():
    user = User.objects.create_user(username='testuser', password='password123', email='testuser@example.com')
    expected_fields = {'id': user.id, 'username': 'testuser', 'email': 'testuser@example.com'}
    
    result = model_to_dict(user)
    
    assert result == expected_fields

@pytest.mark.django_db
def test_model_to_dict_no_editable_fields():
    user = User.objects.create_user(username='testuser', password='password123', email='testuser@example.com')
    
    # Create a field that is not editable by subclassing User
    class NonEditableUser(User):
        class Meta:
            proxy = True
    
    non_editable_user = NonEditableUser.objects.create(username='noneditableuser')
    
    result = model_to_dict(non_editable_user)

    # Assert that result is an empty dict as there are no editable fields
    assert result == {}

@pytest.mark.django_db
def test_model_to_dict_with_empty_fields_and_exclude():
    user = User.objects.create_user(username='testuser', password='password123')
    
    result = model_to_dict(user, fields=[], exclude=['email'])

    # Expecting empty dict since no fields are specified and all are excluded
    assert result == {}