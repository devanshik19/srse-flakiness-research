import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.admin.sites import site
from django.http import HttpResponseRedirect
from django.test import RequestFactory
from django.contrib.admin import ModelAdmin

# A simple ModelAdmin subclass for testing
class TestModelAdmin(ModelAdmin):
    def changeform_view(self, request, object_id, form_url='', extra_context=None):
        return HttpResponseRedirect(reverse('admin:auth_user_change', args=(object_id,)))

# Test cases for the change_view method
@pytest.mark.parametrize("object_id, expected_url", [
    (1, "/admin/auth/user/1/change/"),
])
def test_change_view(object_id, expected_url):
    # Create a user and assign permissions
    user = User.objects.create_user(username='admin', password='password')
    user.is_superuser = True
    user.is_staff = True
    user.save()
    
    # Simulate login
    request = RequestFactory().get('/admin/auth/user/')
    request.user = user
    
    # Create an instance of the test ModelAdmin
    admin = TestModelAdmin(User, site)
    
    # Call the change_view method
    response = admin.change_view(request, object_id)
    
    # Assert that the response redirects to the expected URL
    assert isinstance(response, HttpResponseRedirect)
    assert response['Location'] == expected_url

def test_change_view_not_found():
    user = User.objects.create_user(username='admin', password='password')
    user.is_superuser = True
    user.is_staff = True
    user.save()

    request = RequestFactory().get('/admin/auth/user/')
    request.user = user

    admin = TestModelAdmin(User, site)

    with pytest.raises(Http404):
        admin.change_view(request, 999)  # Assuming 999 does not exist