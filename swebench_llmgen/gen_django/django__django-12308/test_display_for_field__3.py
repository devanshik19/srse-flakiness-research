import pytest
from django.contrib.auth.models import User
from django.db import models
from django.utils import formats, timezone
from django.utils.html import format_html
from django.utils.translation import override as translation_override
from django.contrib.admin.utils import display_for_field

@pytest.mark.parametrize("value, field, empty_value_display, expected", [
    (None, models.BooleanField(), 'N/A', 'N/A'),
    (True, models.BooleanField(), 'N/A', '✓'),
    (False, models.BooleanField(), 'N/A', '✗'),
    (datetime.datetime(2023, 1, 1, 12, 0), models.DateTimeField(), 'N/A', formats.localize(timezone.template_localtime(datetime.datetime(2023, 1, 1, 12, 0)))),
    (None, models.DateField(), 'N/A', 'N/A'),
    (datetime.date(2023, 1, 1), models.DateField(), 'N/A', formats.localize(datetime.date(2023, 1, 1))),
    (None, models.DecimalField(decimal_places=2,), 'N/A', 'N/A'),
    (decimal.Decimal('12.34'), models.DecimalField(decimal_places=2,), 'N/A', formats.number_format(decimal.Decimal('12.34'), 2)),
    (10, models.IntegerField(), 'N/A', formats.number_format(10)),
    (10.5, models.FloatField(), 'N/A', formats.number_format(10.5)),
    (None, models.FileField(), 'N/A', 'N/A'),
    (User.objects.create(username='user1'), models.FileField(), 'N/A', format_html('<a href="{}">{}</a>', User.objects.create(username='user1').url, 'user1')),
    (None, models.CharField(max_length=255), 'N/A', 'N/A'),
    ('Example', models.CharField(max_length=255), 'N/A', 'Example'),
])
def test_display_for_field(value, field, empty_value_display, expected):
    field_instance = field()  # Create an instance of the field
    result = display_for_field(value, field_instance, empty_value_display)
    assert result == expected