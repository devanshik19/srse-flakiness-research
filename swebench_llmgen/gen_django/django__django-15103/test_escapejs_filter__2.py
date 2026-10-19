import pytest
from django.utils.html import escapejs
from django.template.defaultfilters import escapejs_filter

def test_escapejs_filter():
    # Test with a simple string
    assert escapejs_filter("Hello 'World'") == escapejs("Hello 'World'")

    # Test with special characters
    assert escapejs_filter("Line1\nLine2") == escapejs("Line1\nLine2")
    assert escapejs_filter("Tab\tCharacter") == escapejs("Tab\tCharacter")
    assert escapejs_filter("\"Double Quotes\"") == escapejs("\"Double Quotes\"")

    # Test with a string containing a backslash
    assert escapejs_filter("Backslash \\") == escapejs("Backslash \\")

    # Test with an empty string
    assert escapejs_filter("") == escapejs("")

    # Test with a string containing a single quote and double quote
    assert escapejs_filter("It's a \"test\"") == escapejs("It's a \"test\"")

    # Test if the function handles large input
    long_string = "a" * 1000 + "b" * 1000
    assert escapejs_filter(long_string) == escapejs(long_string)