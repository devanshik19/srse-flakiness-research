import datetime
import decimal
from django.contrib.auth.models import User
from django.contrib.admin.utils import display_for_field
from django.db import models
from django.utils import formats
from django.utils.html import format_html

def test_display_for_field():
    empty_value_display = 'N/A'
    
    # Test flatchoices
    class TestField:
        flatchoices = [(1, 'Choice 1'), (2, 'Choice 2')]

    field_with_choices = TestField()
    assert display_for_field(1, field_with_choices, empty_value_display) == 'Choice 1'
    assert display_for_field(3, field_with_choices, empty_value_display) == empty_value_display

    # Test BooleanField
    class BooleanField(models.BooleanField):
        pass

    field_boolean = BooleanField()
    assert display_for_field(True, field_boolean, empty_value_display) == '✓'
    assert display_for_field(False, field_boolean, empty_value_display) == '✗'
    assert display_for_field(None, field_boolean, empty_value_display) == '✗'

    # Test DateTimeField
    field_datetime = models.DateTimeField()
    now = timezone.now()
    formatted_datetime = formats.localize(timezone.template_localtime(now))
    assert display_for_field(now, field_datetime, empty_value_display) == formatted_datetime

    # Test DateField
    field_date = models.DateField()
    today = datetime.date.today()
    assert display_for_field(today, field_date, empty_value_display) == formats.localize(today)

    # Test TimeField
    field_time = models.TimeField()
    current_time = datetime.time.now()
    assert display_for_field(current_time, field_time, empty_value_display) == formats.localize(current_time)

    # Test DecimalField
    decimal_value = decimal.Decimal('123.456')
    field_decimal = models.DecimalField(decimal_places=2, max_digits=5)
    assert display_for_field(decimal_value, field_decimal, empty_value_display) == '123.46'

    # Test IntegerField
    integer_value = 100
    field_integer = models.IntegerField()
    assert display_for_field(integer_value, field_integer, empty_value_display) == '100'

    # Test FloatField
    float_value = 99.99
    field_float = models.FloatField()
    assert display_for_field(float_value, field_float, empty_value_display) == '99.99'

    # Test FileField
    class FakeFile:
        url = 'http://example.com/file'
        
    field_file = models.FileField()
    fake_file = FakeFile()
    assert display_for_field(fake_file, field_file, empty_value_display) == format_html('<a href="{}">{}</a>', fake_file.url, fake_file)

    # Test generic case
    assert display_for_field('Some Value', None, empty_value_display) == 'Some Value'
    assert display_for_field(None, None, empty_value_display) == empty_value_display