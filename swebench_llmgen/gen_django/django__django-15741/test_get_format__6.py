import pytest
from django.conf import settings
from django.utils.formats import get_format

@pytest.mark.parametrize("format_type, lang, use_l10n, expected", [
    ('DATE_FORMAT', None, None, settings.DATE_FORMAT),
    ('TIME_FORMAT', None, None, settings.TIME_FORMAT),
    ('DATETIME_FORMAT', None, None, settings.DATETIME_FORMAT),
    ('DATE_FORMAT', 'en', True, None),  # Expected to fetch from format_modules
    ('INVALID_FORMAT', None, None, 'INVALID_FORMAT'),  # edge case for invalid format
])
def test_get_format(format_type, lang, use_l10n, expected, settings):
    # Adjust settings for this test
    settings.USE_L10N = True
    settings.DATE_FORMAT = 'Y-m-d'
    settings.TIME_FORMAT = 'H:i:s'
    settings.DATETIME_FORMAT = 'Y-m-d H:i:s'
    settings._USE_L10N_INTERNAL = True

    # Prepare the format_modules mock
    import sys
    from unittest.mock import MagicMock

    # Mocking format modules dynamically
    mock_module = MagicMock()
    sys.modules['myapp.formats.en'] = mock_module
    mock_module.DATE_FORMAT = 'd/m/Y' if lang == 'en' else None

    # Call the function
    result = get_format(format_type, lang, use_l10n)

    if expected is None:
        # Validate that the format module was accessed
        if lang == 'en':
            mock_module.DATE_FORMAT.assert_called_once()
        assert result == 'd/m/Y'  # Expect to return mocked value
    else:
        assert result == expected

    # Clean up mock
    del sys.modules['myapp.formats.en']