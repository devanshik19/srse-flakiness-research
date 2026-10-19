import pytest
from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import RequestFactory

class TestModelAdmin(admin.ModelAdmin):
    model = User

@pytest.fixture
def model_admin():
    return TestModelAdmin(User, admin.site)

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpassword')

def test_change_view_get(model_admin, user):
    request = RequestFactory().get(reverse('admin:auth_user_change', args=[user.id]))
    response = model_admin.change_view(request, user.id)
    assert response.status_code == 200
    assert 'Change user' in response.content.decode()

def test_change_view_post(model_admin, user):
    request = RequestFactory().post(reverse('admin:auth_user_change', args=[user.id]), {
        'username': 'changeduser',
        'password': 'newpassword',
    })
    response = model_admin.change_view(request, user.id)
    assert response.status_code == 302
    updated_user = User.objects.get(id=user.id)
    assert updated_user.username == 'changeduser'