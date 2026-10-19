import pytest
from django.contrib.auth.models import User
from django.db import models
from django.utils import formats, timezone
from django.utils.html import format_html
from django.contrib.admin.templatetags.admin_list import _boolean_icon
from django.contrib.admin.utils import display_for_field

def test_display_for_field_choices():
    field = models.CharField(max_length=10, choices=[('a', 'Option A'), ('b', 'Option B')])
    assert display_for_field('a', field, '-') == 'Option A'
    assert display_for_field('b', field, '-') == 'Option B'
    assert display_for_field('c', field, '-') == '-'

def test_display_for_field_boolean():
    field = models.BooleanField()
    assert display_for_field(True, field, '-') == _boolean_icon(True)
    assert display_for_field(False, field, '-') == _boolean_icon(False)
    assert display_for_field(None, field, '-') == _boolean_icon(False)

def test_display_for_field_none_value():
    field = models.CharField(max_length=10)
    assert display_for_field(None, field, '-') == '-'

def test_display_for_field_datetime():
    field = models.DateTimeField()
    dt = timezone.now()
    assert display_for_field(dt, field, '-') == formats.localize(timezone.template_localtime(dt))

def test_display_for_field_date():
    field = models.DateField()
    date = timezone.now().date()
    assert display_for_field(date, field, '-') == formats.localize(date)

def test_display_for_field_time():
    field = models.TimeField()
    time = timezone.now().time()
    assert display_for_field(time, field, '-') == formats.localize(time)

def test_display_for_field_decimal():
    field = models.DecimalField(max_digits=5, decimal_places=2)
    assert display_for_field(decimal.Decimal('12.34'), field, '-') == '12.34'
    assert display_for_field(decimal.Decimal('5.1'), field, '-') == '5.10'

def test_display_for_field_integer():
    field = models.IntegerField()
    assert display_for_field(10, field, '-') == '10'
    assert display_for_field(0, field, '-') == '0'

def test_display_for_field_float():
    field = models.FloatField()
    assert display_for_field(10.1, field, '-') == '10.1'
    assert display_for_field(0.0, field, '-') == '0.0'

def test_display_for_field_file():
    class MockFile:
        url = 'http://example.com/file.txt'
        def __str__(self):
            return 'file.txt'
    
    field = models.FileField()
    file_value = MockFile()
    assert display_for_field(file_value, field, '-') == format_html('<a href="{}">{}</a>', file_value.url, file_value)

def test_display_for_field_json():
    field = models.JSONField()
    json_value = {'key': 'value'}
    assert display_for_field(json_value, field, '-') == json_value