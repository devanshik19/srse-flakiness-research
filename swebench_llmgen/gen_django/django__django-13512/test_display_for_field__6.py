import pytest
from django.contrib.auth.models import User
from django.db import models
from django.utils import formats, timezone
from django.utils.html import format_html
from django.contrib.admin.utils import display_for_field

@pytest.mark.parametrize("field, value, expected", [
    (models.BooleanField(), True, '<img src="/static/admin/img/icon-yes.svg" alt="True" />'),
    (models.BooleanField(), False, '<img src="/static/admin/img/icon-no.svg" alt="False" />'),
    (models.IntegerField(), 5, '5'),
    (models.DecimalField(decimal_places=2), decimal.Decimal('10.50'), '10.50'),
    (models.DateField(), timezone.now().date(), formats.date_format(timezone.now().date())),
    (models.DateTimeField(), timezone.now(), formats.localize(timezone.template_localtime(timezone.now()))),
    (models.FileField(), User.objects.create(username='test_user').profile.create_file('test.txt'), 
     format_html('<a href="{}">{}</a>', User.objects.create(username='test_user').profile.file.url, 'test.txt')),
    (models.JSONField(), {'key': 'value'}, '{"key": "value"}'),
    (models.CharField(max_length=255), '', 'N/A'),  # for empty value scenario
])
def test_display_for_field(field, value, expected):
    empty_value_display = 'N/A'
    assert display_for_field(value, field, empty_value_display) == expected

def test_display_for_field_with_flatchoices():
    field = models.CharField(max_length=255, choices=[('1', 'Choice 1'), ('2', 'Choice 2')])
    value = '1'
    expected = 'Choice 1'
    assert display_for_field(value, field, 'N/A') == expected

    value = '3'
    assert display_for_field(value, field, 'N/A') == 'N/A'  # testing value not in choices