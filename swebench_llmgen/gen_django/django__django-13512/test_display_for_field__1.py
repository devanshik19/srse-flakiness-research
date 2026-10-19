import pytest
import datetime
import decimal
from django.contrib.admin.utils import display_for_field
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

def test_display_for_field_flat_choices():
    field = models.ChoiceField(choices=[(1, 'Choice 1'), (2, 'Choice 2')])
    assert display_for_field(1, field, 'N/A') == 'Choice 1'
    assert display_for_field(2, field, 'N/A') == 'Choice 2'
    assert display_for_field(3, field, 'N/A') == 'N/A'

def test_display_for_field_boolean_field():
    field = models.BooleanField()
    assert display_for_field(True, field, 'N/A') == '✓'
    assert display_for_field(False, field, 'N/A') == '✗'
    assert display_for_field(None, field, 'N/A') == '✗'  # Special handling

def test_display_for_field_none_value():
    field = models.IntegerField()
    assert display_for_field(None, field, 'N/A') == 'N/A'

def test_display_for_field_datetime_field():
    field = models.DateTimeField()
    dt = timezone.now()
    assert display_for_field(dt, field, 'N/A') == formats.localize(timezone.template_localtime(dt))

def test_display_for_field_date_field():
    field = models.DateField()
    date = datetime.date.today()
    assert display_for_field(date, field, 'N/A') == formats.localize(date)

def test_display_for_field_time_field():
    field = models.TimeField()
    time = datetime.datetime.now().time()
    assert display_for_field(time, field, 'N/A') == formats.localize(time)

def test_display_for_field_decimal_field():
    field = models.DecimalField(max_digits=5, decimal_places=2)
    value = decimal.Decimal('10.50')
    assert display_for_field(value, field, 'N/A') == formats.number_format(value, field.decimal_places)

def test_display_for_field_integer_field():
    field = models.IntegerField()
    assert display_for_field(10, field, 'N/A') == formats.number_format(10)

def test_display_for_field_float_field():
    field = models.FloatField()
    assert display_for_field(10.5, field, 'N/A') == formats.number_format(10.5)

def test_display_for_field_file_field():
    field = models.FileField()
    class FileMock:
        url = 'http://example.com/file'

    file_instance = FileMock()
    assert display_for_field(file_instance, field, 'N/A') == '<a href="http://example.com/file">file</a>'

def test_display_for_field_json_field():
    field = models.JSONField()
    value = {'key': 'value'}
    assert display_for_field(value, field, 'N/A') == value  # Assuming get_prep_value returns value as is