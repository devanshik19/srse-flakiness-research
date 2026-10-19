import pytest
from django.conf import settings
from django.utils import translation
from django.contrib.auth.models import User
from django.utils.formats import get_format

@pytest.mark.parametrize("format_type, lang, use_l10n, expected", [
    ("DATE_FORMAT", None, None, settings.DATE_FORMAT),
    ("TIME_FORMAT", None, None, settings.TIME_FORMAT),
    ("DATETIME_FORMAT", None, None, settings.DATETIME_FORMAT),
    ("DATE_FORMAT", "en", None, "F j, Y"),  # Assuming English date format
    ("DATE_FORMAT", "fr", True, "j F Y"),   # Assuming French date format
    ("TIME_FORMAT", "de", True, "H:i"),      # Assuming German time format
])
def test_get_format(format_type, lang, use_l10n, expected):
    if lang:
        translation.activate(lang)

    result = get_format(format_type, lang, use_l10n)

    assert result == expected

def test_get_format_with_cache():
    format_type = "DATE_FORMAT"
    lang = None
    use_l10n = None
    
    first_call = get_format(format_type, lang, use_l10n)
    second_call = get_format(format_type, lang, use_l10n)

    assert first_call == second_call  # Check that the cache is being used