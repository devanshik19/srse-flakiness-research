import pytest
from django.contrib.admin import ModelAdmin
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import RequestFactory

class TestModelAdmin(ModelAdmin):
    change_form_template = 'admin/change_form.html'

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='password')

@pytest.fixture
def request_factory():
    return RequestFactory()

def test_change_view(user, request_factory):
    admin = TestModelAdmin(model=User, admin_site=None)
    object_id = user.id
    request = request_factory.get(reverse('admin:auth_user_change', args=[object_id]))
    request.user = user

    response = admin.change_view(request, object_id)

    assert response.status_code == 200
    assert 'admin/change_form.html' in response.template_name