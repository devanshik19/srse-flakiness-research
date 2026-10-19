import datetime
import decimal
from collections import defaultdict
from django.contrib.auth.models import User
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.forms.utils import pretty_name
from django.utils import formats, timezone
from django.utils.html import format_html
from django.utils.translation import ngettext, override as translation_override
from django.contrib.admin.utils import display_for_field

def test_display_for_field():
    # Setup
    user = User(username='testuser')
    user.save()
    empty_value_display = 'No Value'

    # Test for flatchoices
    field_with_choices = models.CharField(max_length=10, choices=[('A', 'Choice A'), ('B', 'Choice B')])
    assert display_for_field('A', field_with_choices, empty_value_display) == 'Choice A'
    assert display_for_field('C', field_with_choices, empty_value_display) == empty_value_display

    # Test for BooleanField
    boolean_field = models.BooleanField()
    assert display_for_field(True, boolean_field, empty_value_display) == '✓'
    assert display_for_field(False, boolean_field, empty_value_display) == '✗'
    assert display_for_field(None, boolean_field, empty_value_display) == '✗'

    # Test for DateTimeField
    datetime_field = models.DateTimeField()
    now = timezone.now()
    assert display_for_field(now, datetime_field, empty_value_display) == formats.localize(timezone.template_localtime(now))

    # Test for DateField
    date_field = models.DateField()
    today = datetime.date.today()
    assert display_for_field(today, date_field, empty_value_display) == formats.localize(today)

    # Test for TimeField
    time_field = models.TimeField()
    current_time = datetime.datetime.now().time()
    assert display_for_field(current_time, time_field, empty_value_display) == formats.localize(current_time)

    # Test for DecimalField
    decimal_field = models.DecimalField(max_digits=5, decimal_places=2)
    decimal_value = decimal.Decimal('12.34')
    assert display_for_field(decimal_value, decimal_field, empty_value_display) == formats.number_format(decimal_value, decimal_places=2)

    # Test for IntegerField
    integer_field = models.IntegerField()
    integer_value = 123
    assert display_for_field(integer_value, integer_field, empty_value_display) == formats.number_format(integer_value)

    # Test for FloatField
    float_field = models.FloatField()
    float_value = 123.456
    assert display_for_field(float_value, float_field, empty_value_display) == formats.number_format(float_value)

    # Test for FileField
    class DummyFile:
        url = 'http://example.com/file'

    file_field = models.FileField()
    assert display_for_field(DummyFile(), file_field, empty_value_display) == format_html('<a href="{}">{}</a>', DummyFile().url, DummyFile())

    # Test for other types
    assert display_for_field('Some other value', None, empty_value_display) == 'Some other value'
    assert display_for_field(None, None, empty_value_display) == empty_value_display