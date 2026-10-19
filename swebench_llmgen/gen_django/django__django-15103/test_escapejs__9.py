import pytest
from django.utils.html import escapejs
from django.utils.safestring import mark_safe

def test_escapejs():
    # Test normal string
    assert escapejs("Hello World") == mark_safe("Hello World")
    
    # Test special characters that need escaping
    assert escapejs("Quotes: ' \" \\") == mark_safe("Quotes: ' \" \\")
    assert escapejs("<tag>") == mark_safe("<tag>")
    assert escapejs("Backslash: \\") == mark_safe("Backslash: \\")
    
    # Test unicode characters
    assert escapejs("Unicode: \u201c”)") == mark_safe("Unicode: \u201c”)")

    # Test empty string
    assert escapejs("") == mark_safe("")
    
    # Test string with control characters
    assert escapejs("Control: \n\t") == mark_safe("Control: \n\t")
    
    # Test long string
    long_string = "A" * 1000
    assert escapejs(long_string) == mark_safe(long_string)