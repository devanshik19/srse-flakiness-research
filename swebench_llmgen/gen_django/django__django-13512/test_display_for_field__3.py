import pytest
from django.contrib.auth.models import User
from django.db import models
from django.utils import formats, timezone
from django.utils.html import format_html
from django.contrib.admin.utils import display_for_field

@pytest.mark.parametrize("field, value, expected", [
    (models.BooleanField(), True, '<span class="yes">✔</span>'),
    (models.BooleanField(), False, '<span class="no">✖</span>'),
    (models.DateTimeField(), timezone.now(), formats.localize(timezone.template_localtime(timezone.now()))),
    (models.DateField(), timezone.now().date(), formats.localize(timezone.now().date())),
    (models.TimeField(), timezone.now().time(), formats.localize(timezone.now().time())),
    (models.DecimalField(decimal_places=2), decimal.Decimal('123.456'), '123.46'),
    (models.IntegerField(), 123, '123'),
    (models.FloatField(), 123.456, '123.46'),
    (models.FileField(), User(username='testuser').save() or User.objects.get(username='testuser').profile_image, format_html('<a href="{}">{}</a>', User.objects.get(username='testuser').profile_image.url, User.objects.get(username='testuser').profile_image)),
    (models.JSONField(), {"key": "value"}, '{"key": "value"}'),  # Assuming proper prep value return
    (models.JSONField(), None, 'None'),
    (models.CharField(max_length=255), 'test', 'test'),
    (models.EmailField(), None, 'None'),
])
def test_display_for_field(field, value, expected):
    if field.flatchoices:
        field.flatchoices = [(1, 'Choice1'), (2, 'Choice2')]
    result = display_for_field(value, field, 'None')
    assert result == expected