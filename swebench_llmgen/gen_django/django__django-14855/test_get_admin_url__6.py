import pytest
from django.contrib.admin.helpers import AdminReadonlyField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.html import format_html

class DummyForeignKey(models.ForeignKey):
    def __init__(self, *args, **kwargs):
        kwargs['on_delete'] = models.CASCADE
        super().__init__(*args, **kwargs)

@pytest.fixture
def admin_readonly_field():
    form = None
    field = DummyForeignKey(User, related_name='dummy_users')
    is_first = True
    model_admin = None
    return AdminReadonlyField(form, field, is_first, model_admin)

@pytest.fixture
def user_instance():
    return User.objects.create(username='testuser')

def test_get_admin_url_valid(admin_readonly_field, user_instance):
    remote_field = DummyForeignKey(User, related_name='test_field')
    expected_url = reverse('admin:auth_user_change', args=[user_instance.pk])
    
    result = admin_readonly_field.get_admin_url(remote_field, user_instance)
    
    assert result == format_html('<a href="{}">{}</a>', expected_url, user_instance)

def test_get_admin_url_no_reverse_match(admin_readonly_field):
    remote_field = DummyForeignKey(User, related_name='non_existent_field')
    class InvalidUser:
        pk = 9999
        def __str__(self):
            return 'Invalid User'
    
    result = admin_readonly_field.get_admin_url(remote_field, InvalidUser())
    
    assert result == 'Invalid User'