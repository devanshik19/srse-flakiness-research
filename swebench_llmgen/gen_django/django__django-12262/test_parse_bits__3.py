import pytest
from django.template.library import parse_bits
from django.template import Template
from django.template.base import TokenParser
from django.template.exceptions import TemplateSyntaxError

def test_parse_bits_valid_positional_and_keyword():
    parser = TokenParser()
    bits = ['arg1', 'arg2', 'key=value']
    params = ['arg1', 'arg2']
    varargs = None
    varkw = None
    defaults = None
    kwonly = []
    kwonly_defaults = []
    takes_context = False
    name = 'my_tag'

    args, kwargs = parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)
    
    assert args == ['arg1', 'arg2']
    assert kwargs == {'key': 'value'}

def test_parse_bits_with_context_first_param():
    parser = TokenParser()
    bits = ['context', 'arg1', 'key=value']
    params = ['context', 'arg1']
    varargs = None
    varkw = None
    defaults = None
    kwonly = []
    kwonly_defaults = []
    takes_context = True
    name = 'my_tag'

    args, kwargs = parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)

    assert args == ['arg1']
    assert kwargs == {'key': 'value'}

def test_parse_bits_missing_context_with_takes_context():
    parser = TokenParser()
    bits = ['arg1', 'key=value']
    params = ['arg1']
    varargs = None
    varkw = None
    defaults = None
    kwonly = []
    kwonly_defaults = []
    takes_context = True
    name = 'my_tag'

    with pytest.raises(TemplateSyntaxError) as excinfo:
        parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)
    
    assert "'my_tag' is decorated with takes_context=True so it must have a first argument of 'context'" in str(excinfo.value)

def test_parse_bits_unexpected_keyword():
    parser = TokenParser()
    bits = ['arg1', 'key=value']
    params = ['arg1']
    varargs = None
    varkw = None
    defaults = None
    kwonly = []
    kwonly_defaults = []
    takes_context = False
    name = 'my_tag'

    with pytest.raises(TemplateSyntaxError) as excinfo:
        parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)
    
    assert "'my_tag' received unexpected keyword argument 'key'" in str(excinfo.value)

def test_parse_bits_multiple_values_for_keyword():
    parser = TokenParser()
    bits = ['arg1', 'key=value', 'key=another_value']
    params = ['arg1']
    varargs = None
    varkw = None
    defaults = None
    kwonly = []
    kwonly_defaults = []
    takes_context = False
    name = 'my_tag'

    with pytest.raises(TemplateSyntaxError) as excinfo:
        parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)
    
    assert "'my_tag' received multiple values for keyword argument 'key'" in str(excinfo.value)

def test_parse_bits_positional_after_keyword():
    parser = TokenParser()
    bits = ['key=value', 'arg1']
    params = ['arg1']
    varargs = None
    varkw = None
    defaults = None
    kwonly = []
    kwonly_defaults = []
    takes_context = False
    name = 'my_tag'

    with pytest.raises(TemplateSyntaxError) as excinfo:
        parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)
    
    assert "'my_tag' received some positional argument(s) after some keyword argument(s)" in str(excinfo.value)

def test_parse_bits_too_many_positional_arguments():
    parser = TokenParser()
    bits = ['arg1', 'arg2', 'arg3']
    params = ['arg1', 'arg2']
    varargs = None
    varkw = None
    defaults = None
    kwonly = []
    kwonly_defaults = []
    takes_context = False
    name = 'my_tag'

    with pytest.raises(TemplateSyntaxError) as excinfo:
        parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)
    
    assert "'my_tag' received too many positional arguments" in str(excinfo.value)

def test_parse_bits_missing_positional_arguments():
    parser = TokenParser()
    bits = ['arg1']
    params = ['arg1', 'arg2']
    varargs = None
    varkw = None
    defaults = None
    kwonly = []
    kwonly_defaults = []
    takes_context = False
    name = 'my_tag'

    with pytest.raises(TemplateSyntaxError) as excinfo:
        parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)

    assert "'my_tag' did not receive value(s) for the argument(s): 'arg2'" in str(excinfo.value)