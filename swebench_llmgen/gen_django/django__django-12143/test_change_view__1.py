import json
import pytest
from django.contrib import admin
from django.contrib.auth.models import User
from django.http import HttpRequest

@pytest.fixture
def admin_user(db):
    user = User.objects.create_user(username='admin', password='password')
    user.is_staff = True
    user.is_superuser = True
    user.save()
    return user

@pytest.fixture
def model_admin():
    class TestModelAdmin(admin.ModelAdmin):
        model = User

        def changeform_view(self, request, object_id, form_url='', extra_context=None):
            # Simulating the original function call
            return super().changeform_view(request, object_id, form_url, extra_context)
    
    return TestModelAdmin(User, admin.site)

def test_change_view(admin_user, model_admin):
    request = HttpRequest()
    request.user = admin_user
    request.method = 'GET'

    # Creating a user instance to change
    user_instance = User.objects.create_user(username='test_user', password='password123')

    response = model_admin.change_view(request, user_instance.id)

    assert response.status_code == 200
    assert isinstance(response, admin.views.decorators.csrf_protect)  # Assuming this decorator is relevant for change form view
    assert 'Change' in response.content.decode()  # Assert the presence of change in response content