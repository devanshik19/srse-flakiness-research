import pytest
from django.contrib.admin.utils import display_for_field
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.html import format_html


def test_display_for_field_flat_choices():
    class FlatChoiceField:
        flatchoices = [(1, 'One'), (2, 'Two')]

    field = FlatChoiceField()
    assert display_for_field(1, field, 'N/A') == 'One'
    assert display_for_field(2, field, 'N/A') == 'Two'
    assert display_for_field(3, field, 'N/A') == 'N/A'

def test_display_for_field_boolean_field():
    class BooleanField:
        pass

    field = BooleanField()
    
    assert display_for_field(True, field, 'N/A') == '✓'
    assert display_for_field(False, field, 'N/A') == '✗'

def test_display_for_field_none_value():
    class BasicField:
        pass

    field = BasicField()
    assert display_for_field(None, field, 'N/A') == 'N/A'

def test_display_for_field_datetime_field():
    class DateTimeField:
        pass

    field = DateTimeField()
    value = timezone.now()
    assert display_for_field(value, field, 'N/A') == formats.localize(value)

def test_display_for_field_date_field():
    class DateField:
        pass

    field = DateField()
    value = timezone.now().date()
    assert display_for_field(value, field, 'N/A') == formats.localize(value)

def test_display_for_field_time_field():
    class TimeField:
        pass

    field = TimeField()
    value = timezone.now().time()
    assert display_for_field(value, field, 'N/A') == formats.localize(value)

def test_display_for_field_decimal_field():
    class DecimalField:
        decimal_places = 2

    field = DecimalField()
    assert display_for_field(decimal.Decimal('10.1234'), field, 'N/A') == '10.12'

def test_display_for_field_integer_field():
    class IntegerField:
        pass

    field = IntegerField()
    assert display_for_field(10, field, 'N/A') == '10'

def test_display_for_field_float_field():
    class FloatField:
        pass

    field = FloatField()
    assert display_for_field(10.5, field, 'N/A') == '10.5'

def test_display_for_field_file_field():
    class FileField:
        def __init__(self, url):
            self.url = url

    field = FileField(url='/media/testfile.txt')
    assert display_for_field(field, field, 'N/A') == format_html('<a href="{}">{}</a>', field.url, field)

def test_display_for_field_json_field():
    class JSONField:
        def get_prep_value(self, value):
            return str(value)

    field = JSONField()
    assert display_for_field({'key': 'value'}, field, 'N/A') == str({'key': 'value'})