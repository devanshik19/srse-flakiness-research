import pytest
from django.contrib.auth.models import User
from django.db import models
from django.utils import formats, timezone
from django.utils.html import format_html
from django.contrib.admin.utils import display_for_field

@pytest.mark.parametrize("field, value, expected", [
    (models.CharField(max_length=100, choices=[('A', 'Choice A')]), 'A', 'Choice A'),
    (models.CharField(max_length=100), None, ''),
    (models.BooleanField(), True, format_html('<img src="boolean-true.png" alt="True" />')),
    (models.BooleanField(), False, format_html('<img src="boolean-false.png" alt="False" />')),
    (models.DateTimeField(), timezone.now(), formats.localize(timezone.template_localtime(timezone.now()))),
    (models.DateField(), timezone.now().date(), formats.localize(timezone.now().date())),
    (models.TimeField(), timezone.now().time(), formats.localize(timezone.now().time())),
    (models.DecimalField(max_digits=5, decimal_places=2), decimal.Decimal('123.45'), '123.45'),
    (models.IntegerField(), 42, '42'),
    (models.FloatField(), 3.14, '3.14'),
    (models.FileField(), User.objects.create(username='testuser', password='password').default_storage.save('test.txt', b'test content'), '<a href="{}">test.txt</a>'.format(User.objects.get(username='testuser').default_storage.url('test.txt'))),
    (models.JSONField(), {"key": "value"}, '{"key": "value"}'),
])
def test_display_for_field(field, value, expected):
    # Create a field instance
    field_instance = field()
    result = display_for_field(value, field_instance, 'N/A')
    assert result == expected

def test_display_for_field_empty(value=None):
    field = models.CharField(max_length=100)
    result = display_for_field(value, field, 'N/A')
    assert result == 'N/A'