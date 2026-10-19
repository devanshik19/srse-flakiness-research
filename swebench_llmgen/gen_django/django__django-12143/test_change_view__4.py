import pytest
from django.contrib.admin.sites import site
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpRequest
from django.contrib.admin import ModelAdmin

@pytest.mark.django_db
def test_change_view():
    # Create a user and assign permissions
    user = User.objects.create_user(username='testuser', password='testpass')
    user.is_superuser = True
    user.is_staff = True
    user.save()

    # Create a request with the user
    request = HttpRequest()
    request.user = user

    # Create a ModelAdmin instance
    model_admin = ModelAdmin(model=User, admin_site=site)

    # Create a User instance to be edited
    user_instance = User.objects.create(username='testuser2', password='testpass')

    # Call the change_view method
    response = model_admin.change_view(
        request,
        object_id=user_instance.id,
        form_url='',
        extra_context=None,
    )

    # Assert that the response is a TemplateResponse
    assert isinstance(response, TemplateResponse)

    # Assert that the template context contains the expected object
    assert response.context_data['original'] == user_instance

    # Assert that the correct template is being used
    assert 'admin/auth/user/change.html' in response.template_name