import pytest
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

@pytest.mark.django_db
def test_model_to_dict_full():
    user = User.objects.create_user(username='testuser', password='password123', email='test@example.com')
    result = model_to_dict(user)
    assert result['username'] == 'testuser'
    assert result['email'] == 'test@example.com'
    assert 'password' not in result  # Password is not included

@pytest.mark.django_db
def test_model_to_dict_with_fields():
    user = User.objects.create_user(username='testuser', password='password123', email='test@example.com')
    result = model_to_dict(user, fields=['username', 'email'])
    assert result['username'] == 'testuser'
    assert result['email'] == 'test@example.com'
    assert 'password' not in result

@pytest.mark.django_db
def test_model_to_dict_with_exclude():
    user = User.objects.create_user(username='testuser', password='password123', email='test@example.com')
    result = model_to_dict(user, exclude=['password', 'email'])
    assert result['username'] == 'testuser'
    assert 'email' not in result
    assert 'password' not in result

@pytest.mark.django_db
def test_model_to_dict_with_fields_and_exclude():
    user = User.objects.create_user(username='testuser', password='password123', email='test@example.com')
    result = model_to_dict(user, fields=['username', 'email'], exclude=['email'])
    assert result['username'] == 'testuser'
    assert 'email' not in result