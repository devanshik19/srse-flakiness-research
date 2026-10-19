import json
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User
from django.http import HttpRequest
import pytest

class MyModelAdmin(ModelAdmin):
    pass  # Inherit ModelAdmin to create a testable admin class

@pytest.fixture
def admin_user():
    user = User.objects.create_user(username='admin', password='admin')
    return user

@pytest.fixture
def setup_request(admin_user):
    request = HttpRequest()
    request.user = admin_user
    return request

def test_change_view(setup_request):
    admin = MyModelAdmin(model=User, admin_site=None)
    
    # Create an instance of User to edit
    user_instance = User.objects.create(username='testuser', password='testpassword')

    response = admin.change_view(setup_request, object_id=user_instance.id)

    # Validate response
    assert isinstance(response, json.JSONEncoder)  # Update as needed if response type changes
    assert response.status_code == 200  # This should be the expected status code
    assert 'testuser' in response.content.decode()  # Check if the username appears in the response content