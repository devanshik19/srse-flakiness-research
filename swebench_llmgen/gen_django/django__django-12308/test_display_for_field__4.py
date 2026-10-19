import pytest
from django.contrib.auth.models import User
from django.db import models
from django.utils import formats, timezone
from django.utils.html import format_html
from django.utils.translation import ngettext
from django.contrib.admin.utils import display_for_field

@pytest.mark.parametrize("field, value, expected", [
    (models.BooleanField(), True, '<img alt="True" src="/static/admin/img/icon-yes.svg" />'),
    (models.BooleanField(), False, '<img alt="False" src="/static/admin/img/icon-no.svg" />'),
    (models.DateTimeField(), timezone.now(), formats.localize(timezone.template_localtime(timezone.now()))),
    (models.DateField(), timezone.now().date(), formats.localize(timezone.now().date())),
    (models.TimeField(), timezone.now().time(), formats.localize(timezone.now().time())),
    (models.DecimalField(decimal_places=2), decimal.Decimal('10.1234'), '10.12'),
    (models.IntegerField(), 42, '42'),
    (models.FloatField(), 3.14, '3.14'),
    (models.FileField(), User(username='test_user', email='user@example.com'), format_html('<a href="{}">{}</a>', User(username='test_user', email='user@example.com').url, 'test_user')),
    (models.CharField(), None, 'Empty Value'),
    (models.CharField(), 'Some Value', 'Some Value'),
])
def test_display_for_field(field, value, expected):
    user = User(username='test_user', email='user@example.com')
    empty_value_display = 'Empty Value'
    assert display_for_field(value, field, empty_value_display) == expected