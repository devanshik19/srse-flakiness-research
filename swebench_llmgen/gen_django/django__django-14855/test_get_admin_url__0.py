import pytest
from django.contrib.admin.helpers import AdminReadonlyField
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.urls import NoReverseMatch
from django.utils.html import format_html

@pytest.mark.django_db
def test_get_admin_url_valid():
    user = User.objects.create_user(username='testuser', password='testpassword')
    field = AdminReadonlyField.__init__(None, None, None, None)  # Create an instance
    result = field.get_admin_url(User._meta.get_field('username'), user)
    expected_url = format_html('<a href="{}">{}</a>', f'/admin/auth/user/{user.pk}/change/', user)
    
    assert result == expected_url

@pytest.mark.django_db
def test_get_admin_url_no_reverse_match():
    class DummyRemoteField:
        model = User
        
    class DummyObject:
        pk = 9999  # Assuming a non-existent object

    field = AdminReadonlyField.__init__(None, None, None, None)  # Create an instance
    result = field.get_admin_url(DummyRemoteField(), DummyObject())
    
    assert result == 'DummyObject'