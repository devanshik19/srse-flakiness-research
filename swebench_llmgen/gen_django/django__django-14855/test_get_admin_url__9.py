import pytest
from django.contrib.auth.models import User
from django.contrib.admin.utils import quote
from django.urls import reverse
from django.utils.html import format_html
from django.core.exceptions import ObjectDoesNotExist

class AdminReadonlyField:
    def __init__(self, form, field, is_first, model_admin):
        self.form = form
        self.field = field
        self.is_first = is_first
        self.model_admin = model_admin

    def get_admin_url(self, remote_field, remote_obj):
        url_name = 'admin:%s_%s_change' % (
            remote_field.model._meta.app_label,
            remote_field.model._meta.model_name,
        )
        try:
            url = reverse(url_name, args=[quote(remote_obj.pk)])
            return format_html('<a href="{}">{}</a>', url, remote_obj)
        except NoReverseMatch:
            return str(remote_obj)

@pytest.mark.parametrize("remote_field, remote_obj, expected_output", [
    # Test with a valid field and user object
    (User._meta.get_field('id'), User(username='testuser', pk=1), 
     '<a href="/admin/auth/user/1/change/">testuser</a>'),
    # Additional test case for NoReverseMatch handling
    # Simulating a condition that causes NoReverseMatch
])
def test_get_admin_url(remote_field, remote_obj, expected_output):
    field = AdminReadonlyField(None, None, None, None)
    if remote_field and remote_obj:
        remote_obj.save()
    result = field.get_admin_url(remote_field, remote_obj)
    assert result == expected_output