import pytest
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User
from django.http import HttpRequest


class TestModelAdmin(ModelAdmin):
    def change_view(self, request, object_id, form_url='', extra_context=None):
        return self.changeform_view(request, object_id, form_url, extra_context)


@pytest.fixture
def user_with_permissions(django_user_model):
    user = django_user_model.objects.create_user(username='admin', password='password')
    user.is_superuser = True
    user.is_staff = True
    user.save()
    return user


@pytest.fixture
def admin_instance():
    return TestModelAdmin(User, None)


def test_change_view_redirects_to_changeform_view(admin_instance, user_with_permissions):
    request = HttpRequest()
    request.user = user_with_permissions
    object_id = 1  # Assuming there's a User with ID 1
    form_url = ''
    extra_context = None

    response = admin_instance.change_view(request, object_id, form_url, extra_context)

    assert response.status_code == 302  # Check if it redirects
    assert 'change/' in response.url  # Check if the response URL contains 'change/'


def test_change_view_with_extra_context(admin_instance, user_with_permissions):
    request = HttpRequest()
    request.user = user_with_permissions
    object_id = 1  # Assuming there's a User with ID 1
    form_url = ''
    extra_context = {'title': 'Custom Title'}

    response = admin_instance.change_view(request, object_id, form_url, extra_context)

    assert response.status_code == 302  # Check if it redirects
    assert 'change/' in response.url  # Check if the response URL contains 'change/'
    # Additional test could be adding checks on template context if needed