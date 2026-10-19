import pytest
from django.utils.html import escapejs
from django.template.defaultfilters import escapejs_filter

def test_escapejs_filter():
    # Test with simple strings
    assert escapejs_filter("Hello, World!") == escapejs("Hello, World!")
    assert escapejs_filter('"Quote"') == escapejs('"Quote"')
    assert escapejs_filter("Newline\nCharacter") == escapejs("Newline\nCharacter")
    
    # Test with special characters
    assert escapejs_filter("<script>alert('XSS');</script>") == escapejs("<script>alert('XSS');</script>")
    assert escapejs_filter(u"Unicode: \u03A9") == escapejs(u"Unicode: \u03A9")

    # Test with an empty string
    assert escapejs_filter("") == escapejs("")

    # Test with non-string input
    with pytest.raises(TypeError):
        escapejs_filter(None)
    with pytest.raises(TypeError):
        escapejs_filter(123)
    with pytest.raises(TypeError):
        escapejs_filter(['not', 'a', 'string'])