import pytest
from django.contrib.admindocs.utils import replace_unnamed_groups

def test_replace_unnamed_groups():
    # Test cases to validate the functionality of replace_unnamed_groups
    
    # No unnamed groups in pattern
    assert replace_unnamed_groups(r'^(?P<a>\w+)/b/(?P<name>\w+)$') == r'^(?P<a>\w+)/b/(?P<name>\w+)$'
    
    # Single unnamed group
    assert replace_unnamed_groups(r'^(?P<a>\w+)/b/(\w+)$') == r'^(?P<a>\w+)/b/<var>$'
    
    # Multiple unnamed groups, one named 
    assert replace_unnamed_groups(r'^(?P<a>\w+)/b/((x|y)\w+)$') == r'^(?P<a>\w+)/b/<var>$'
    
    # Nested unnamed groups
    assert replace_unnamed_groups(r'^(?P<a>\w+)/b/(((x|y)\w+))$') == r'^(?P<a>\w+)/b/<var>$'
    
    # Unnamed group immediately following named group
    assert replace_unnamed_groups(r'^(?P<a>\w+)/b/((x|y)\w+)(?P<suffix>\w+)$') == r'^(?P<a>\w+)/b/<var>(?P<suffix>\w+)$'
    
    # Complex pattern with mixed named/unnamed groups
    assert replace_unnamed_groups(r'^(?P<first>\w+)/b/((x|y)\w+)/c/(?P<second>\w+)$') == r'^(?P<first>\w+)/b/<var>/c/(?P<second>\w+)$'
    
    # Pattern with no groups
    assert replace_unnamed_groups(r'^/some/path$') == r'^/some/path$'
    
    # Edge case: empty pattern
    assert replace_unnamed_groups(r'') == r''