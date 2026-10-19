import pytest
from django.contrib.auth.models import User
from django.db import models
from django.utils import formats
from django.utils.html import format_html
from django.utils.translation import ngettext
from django.contrib.admin.utils import display_for_field


@pytest.mark.parametrize("value, field, empty_value_display, expected", [
    ('Choice1', models.CharField(choices=[('Choice1', 'Choice 1'), ('Choice2', 'Choice 2')], max_length=10), 'N/A', 'Choice 1'),
    (True, models.BooleanField(), 'N/A', '✓'),
    (None, models.BooleanField(), 'N/A', 'N/A'),
    (datetime.datetime(2023, 1, 1, 12, 0), models.DateTimeField(), 'N/A', formats.localize(datetime.datetime(2023, 1, 1, 12, 0))),
    (datetime.date(2023, 1, 1), models.DateField(), 'N/A', formats.localize(datetime.date(2023, 1, 1))),
    (decimal.Decimal('10.12345'), models.DecimalField(decimal_places=2, max_digits=5), 'N/A', '10.12'),
    (3.14, models.FloatField(), 'N/A', '3.14'),
    (5, models.IntegerField(), 'N/A', '5'),
    ('test.txt', models.FileField(), 'N/A', format_html('<a href="{}">{}</a>', 'test.txt', 'test.txt')),
    ('Any value', models.TextField(), 'N/A', 'Any value'),
])
def test_display_for_field(value, field, empty_value_display, expected):
    field.flatchoices = getattr(field, 'flatchoices', None)  # Ensure flatchoices is set for params
    assert display_for_field(value, field, empty_value_display) == expected


def test_display_for_field_empty_value():
    field = models.CharField(max_length=10)
    assert display_for_field(None, field, 'N/A') == 'N/A'