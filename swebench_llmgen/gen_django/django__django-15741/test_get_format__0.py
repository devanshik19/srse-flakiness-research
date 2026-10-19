import pytest
from django.conf import settings
from django.utils.formats import get_format

def test_get_format_default_settings():
    settings.DATE_FORMAT = 'Y-m-d'
    assert get_format('DATE_FORMAT') == 'Y-m-d'

def test_get_format_with_localization():
    settings.USE_L10N = True
    settings.DATE_FORMAT = 'd/m/Y'
    assert get_format('DATE_FORMAT', lang='en') == 'd/m/Y'

def test_get_format_without_localization():
    settings.USE_L10N = False
    settings.DATE_FORMAT = 'd/m/Y'
    assert get_format('DATE_FORMAT') == 'd/m/Y'

def test_get_format_invalid_format_type():
    assert get_format('INVALID_FORMAT') == 'INVALID_FORMAT'

def test_get_format_cache_usage():
    settings.DATE_FORMAT = 'Y-m-d'
    first_call = get_format('DATE_FORMAT')
    # This call should hit the cache:
    second_call = get_format('DATE_FORMAT')
    assert first_call is second_call

def test_get_format_falls_back_to_settings():
    settings.DAY_FORMAT = 'm/d/Y'
    assert get_format('DAY_FORMAT') == 'm/d/Y'

def test_get_format_iso_input_formats():
    settings.DATE_INPUT_FORMATS = ['%Y-%m-%d', '%d-%m-%Y']
    settings.USE_L10N = True
    settings.DATE_FORMAT = ['d/m/Y']
    result = get_format('DATE_INPUT_FORMATS')
    assert '%Y-%m-%d' in result
    assert '%d-%m-%Y' in result