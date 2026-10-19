import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpRequest
from django.contrib.admin.sites import site
from django.contrib.admin import ModelAdmin

class TestModelAdmin(ModelAdmin):
    pass

@pytest.fixture
def user(db):
    user = User.objects.create_user(username='admin', password='admin')
    return user

@pytest.fixture
def admin_model():
    return TestModelAdmin(User, site)

@pytest.fixture
def request(user):
    req = HttpRequest()
    req.user = user
    return req

def test_change_view(admin_model, request):
    user_instance = User.objects.create_user(username='testuser', password='testpass')
    url = reverse('admin:auth_user_change', args=[user_instance.id])
    
    response = admin_model.change_view(request, user_instance.id)
    
    assert response.status_code == 200
    assert 'Change' in response.templates[0].name  # Assuming the change_form template is used