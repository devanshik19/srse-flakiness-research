import pytest
from django.contrib.admin import site
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.test import RequestFactory
from django.contrib.admin.options import ModelAdmin

class UserAdmin(ModelAdmin):
    model = User

@pytest.fixture
def user_admin():
    admin = UserAdmin(User, site)
    return admin

@pytest.fixture
def request_factory():
    return RequestFactory()

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpass')

def test_change_view_renders_correct_template(user_admin, request_factory, user):
    url = reverse('admin:auth_user_change', args=[user.id])
    request = request_factory.get(url)
    request.user = user

    response = user_admin.change_view(request, user.id)

    assert isinstance(response, HttpResponseRedirect) is False
    assert 'admin/change_form.html' in response.template_name

def test_change_view_redirects_when_no_permission(user_admin, request_factory):
    # Simulating a user with no permission to change the User model
    user_without_perm = User.objects.create_user(username='nopermuser', password='testpass')
    url = reverse('admin:auth_user_change', args=[1])
    request = request_factory.get(url)
    request.user = user_without_perm

    response = user_admin.change_view(request, 1)

    assert isinstance(response, HttpResponseRedirect)
    assert response.url == '/admin/login/?next=' + url