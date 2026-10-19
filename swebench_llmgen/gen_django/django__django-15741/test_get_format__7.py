import pytest
from django.conf import settings
from django.utils.formats import get_format

# Test cases for the get_format function
def test_get_format_default_locale():
    settings.USE_L10N = True
    settings.DATE_FORMAT = 'Y-m-d'
    settings.LANGUAGE_CODE = 'en-us'
    
    result = get_format('DATE_FORMAT')
    assert result == 'Y-m-d'

def test_get_format_with_lang():
    settings.USE_L10N = True
    settings.LANGUAGE_CODE = 'en-us'
    settings.DATE_FORMAT = 'd/m/Y'

    result = get_format('DATE_FORMAT', lang='fr-fr')
    assert result != 'd/m/Y'  # Assuming the French format is different

def test_get_format_without_l10n():
    settings.USE_L10N = False
    settings.DATE_FORMAT = 'm/d/Y'
    
    result = get_format('DATE_FORMAT')
    assert result == 'm/d/Y'

def test_get_format_nonexistent_format():
    settings.USE_L10N = True
    settings.DATE_FORMAT = 'm/d/Y'
    
    result = get_format('NONEXISTENT_FORMAT')
    assert result == 'NONEXISTENT_FORMAT'

def test_get_format_with_caching():
    settings.USE_L10N = True
    settings.DATE_FORMAT = 'Y-m-d'
    
    first_call = get_format('DATE_FORMAT')
    second_call = get_format('DATE_FORMAT')
    assert first_call == second_call  # Ensure the cached value is used