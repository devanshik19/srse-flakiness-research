import pytest
from django.contrib.auth.models import User
from django.db import models
from django.utils import formats, timezone
from django.utils.html import format_html
from django.utils.translation import ngettext
from django.contrib.admin.utils import display_for_field

@pytest.mark.parametrize("value, field, expected_output", [
    ("Choice1", models.CharField(choices=[("Choice1", "Choice 1"), ("Choice2", "Choice 2")]), "Choice 1"),
    (True, models.BooleanField(), '✓'),
    (None, models.BooleanField(), 'No'),
    (timezone.now(), models.DateTimeField(), formats.localize(timezone.template_localtime(timezone.now()))),
    (timezone.now().date(), models.DateField(), formats.localize(timezone.now().date())),
    (timezone.now().time(), models.TimeField(), formats.localize(timezone.now().time())),
    (decimal.Decimal('123.45'), models.DecimalField(decimal_places=2), '123.45'),
    (123, models.IntegerField(), '123'),
    (123.45, models.FloatField(), '123.45'),
    (User(username="testuser"), models.FileField(), format_html('<a href="{}">{}</a>', User(username="testuser").get_absolute_url(), "testuser")),
    ("SomeValue", models.TextField(), 'SomeValue'),
    (None, models.TextField(), 'No'),
])
def test_display_for_field(value, field, expected_output):
    field_instance = field if isinstance(field, models.Field) else field()
    assert display_for_field(value, field_instance, 'No') == expected_output