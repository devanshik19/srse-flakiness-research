import pytest
from django.utils.html import escape

def test_escape_basic():
    assert escape("Test & < > \" '") == 'Test &amp; &lt; &gt; &quot; &#x27;'
    assert escape("& < >") == '&amp; &lt; &gt;'
    
def test_escape_already_escaped():
    assert escape("&amp; &lt; &gt;") == '&amp; &amp; &lt; &gt;'

def test_escape_special_characters():
    assert escape("Hello 'World'") == 'Hello &#x27;World&#x27;'
    assert escape("Use <b>bold</b>") == 'Use &lt;b&gt;bold&lt;/b&gt;'
    
def test_escape_empty_string():
    assert escape("") == ''

def test_escape_number():
    assert escape(123) == '123'

def test_escape_none():
    assert escape(None) == 'None'