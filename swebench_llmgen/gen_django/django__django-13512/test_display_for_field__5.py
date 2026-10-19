import datetime
import decimal
from collections import defaultdict
from django.contrib.admin.utils import display_for_field
from django.contrib.auth.models import User
from django.db import models
from django.utils import formats, timezone


def test_display_for_field_choices():
    field = models.ChoiceField(choices=[(1, 'Choice 1'), (2, 'Choice 2')])
    assert display_for_field(1, field, 'N/A') == 'Choice 1'
    assert display_for_field(3, field, 'N/A') == 'N/A'


def test_display_for_field_boolean():
    field = models.BooleanField()
    assert display_for_field(True, field, 'N/A') == '✓'
    assert display_for_field(False, field, 'N/A') == '✗'
    assert display_for_field(None, field, 'N/A') == '✗'  # Special NULL handling


def test_display_for_field_empty():
    field = models.CharField(max_length=100)
    assert display_for_field(None, field, 'N/A') == 'N/A'


def test_display_for_field_datetime():
    field = models.DateTimeField()
    dt_value = timezone.now()
    assert display_for_field(dt_value, field, 'N/A') == formats.localize(timezone.template_localtime(dt_value))


def test_display_for_field_date():
    field = models.DateField()
    date_value = datetime.date.today()
    assert display_for_field(date_value, field, 'N/A') == formats.localize(date_value)


def test_display_for_field_time():
    field = models.TimeField()
    time_value = datetime.time(12, 0)
    assert display_for_field(time_value, field, 'N/A') == formats.localize(time_value)


def test_display_for_field_decimal():
    field = models.DecimalField(max_digits=5, decimal_places=2)
    decimal_value = decimal.Decimal('123.45')
    assert display_for_field(decimal_value, field, 'N/A') == formats.number_format(decimal_value, 2)


def test_display_for_field_integer():
    field = models.IntegerField()
    int_value = 42
    assert display_for_field(int_value, field, 'N/A') == formats.number_format(int_value)


def test_display_for_field_float():
    field = models.FloatField()
    float_value = 42.5
    assert display_for_field(float_value, field, 'N/A') == formats.number_format(float_value)


def test_display_for_field_file():
    class FakeFile:
        url = 'http://fakeurl.com/fakefile'
        
    field = models.FileField()
    file_value = FakeFile()
    assert display_for_field(file_value, field, 'N/A') == '<a href="http://fakeurl.com/fakefile">fakefile</a>'

    
def test_display_for_field_json():
    field = models.JSONField()
    json_value = {'key': 'value'}
    assert display_for_field(json_value, field, 'N/A') == json_value