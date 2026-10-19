import pytest
from django.utils import formats
from decimal import Decimal
from django.template.defaultfilters import floatformat

def test_floatformat():
    assert floatformat(34.23234) == formats.number_format("34.2", 1, use_l10n=True, force_grouping=False)
    assert floatformat(34.00000) == formats.number_format("34", 0, use_l10n=True, force_grouping=False)
    assert floatformat(34.26000) == formats.number_format("34.3", 1, use_l10n=True, force_grouping=False)

    assert floatformat(34.23234, 3) == formats.number_format("34.232", 3, use_l10n=True, force_grouping=False)
    assert floatformat(34.00000, 3) == formats.number_format("34.000", 3, use_l10n=True, force_grouping=False)
    assert floatformat(34.26000, 3) == formats.number_format("34.260", 3, use_l10n=True, force_grouping=False)

    assert floatformat(34.23234, -3) == formats.number_format("34.232", 1, use_l10n=True, force_grouping=False)
    assert floatformat(34.00000, -3) == formats.number_format("34", 0, use_l10n=True, force_grouping=False)
    assert floatformat(34.26000, -3) == formats.number_format("34.260", 1, use_l10n=True, force_grouping=False)

    assert floatformat(6666.6666, '2g') == formats.number_format("6,666.67", 2, use_l10n=True, force_grouping=True)
    assert floatformat(10000, 'g') == formats.number_format("10,000", 0, use_l10n=True, force_grouping=True)

    assert floatformat(66666.6666, '2') == formats.number_format("66666.67", 2, use_l10n=False, force_grouping=False)
    assert floatformat(66666.6666, '2u') == formats.number_format("66666.67", 2, use_l10n=False, force_grouping=False)

    assert floatformat(float('inf')) == 'inf'
    assert floatformat(float('-inf')) == '-inf'
    assert floatformat(float('nan')) == 'nan'
    
    assert floatformat("invalid input") == ""
    assert floatformat("") == ""