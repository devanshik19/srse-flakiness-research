import pytest
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.html import format_html
from django.utils import formats
from django.contrib.admin.utils import display_for_field

@pytest.mark.parametrize("field, value, expected_output", [
    (models.CharField(max_length=100, flatchoices=[(1, 'One'), (2, 'Two')]), 1, 'One'),
    (models.BooleanField(), True, '<img src="/static/admin/img/icon-yes.svg" alt="True" />'),
    (models.BooleanField(), False, '<img src="/static/admin/img/icon-no.svg" alt="False" />'),
    (models.DateTimeField(), timezone.now(), formats.localize(timezone.template_localtime(timezone.now()))),
    (models.DateField(), timezone.datetime(2021, 1, 1).date(), formats.localize(timezone.datetime(2021, 1, 1).date())),
    (models.TimeField(), timezone.datetime.now().time(), formats.localize(timezone.datetime.now().time())),
    (models.DecimalField(max_digits=5, decimal_places=2), decimal.Decimal('123.45'), '123.45'),
    (models.IntegerField(), 123, '123'),
    (models.FloatField(), 123.456, '123.46'),
    (models.FileField(), User(username='testuser', email='test@example.com', date_joined=timezone.now()), 
        format_html('<a href="{}">{}</a>', User(username='testuser', email='test@example.com', date_joined=timezone.now()).url, 'testuser')),
    (models.FileField(), None, 'test'),
    (models.CharField(max_length=100), None, 'test'),
])
def test_display_for_field(field, value, expected_output):
    field_instance = field()
    result = display_for_field(value, field_instance, 'test')
    assert result == expected_output