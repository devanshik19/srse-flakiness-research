import pytest
from django.template.library import parse_bits
from django.template.exceptions import TemplateSyntaxError
from django.template import Node

def test_parse_bits_positional_arguments():
    parser = Node()  # Dummy parser for the test
    bits = ['arg1', 'arg2']
    params = ['arg1', 'arg2']
    varargs = None
    varkw = None
    defaults = None
    kwonly = []
    kwonly_defaults = []
    takes_context = False
    name = 'test_tag'

    args, kwargs = parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)
    
    assert args == [parser.compile_filter('arg1'), parser.compile_filter('arg2')]
    assert kwargs == {}

def test_parse_bits_keyword_arguments():
    parser = Node()  # Dummy parser for the test
    bits = ['arg1', 'key=value']
    params = ['arg1']
    varargs = None
    varkw = None
    defaults = None
    kwonly = ['key']
    kwonly_defaults = []
    takes_context = False
    name = 'test_tag'
    
    args, kwargs = parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)

    assert args == [parser.compile_filter('arg1')]
    assert kwargs == {'key': 'value'}

def test_parse_bits_multiple_keyword_arguments():
    parser = Node()  # Dummy parser for the test
    bits = ['arg1', 'key1=value1', 'key2=value2']
    params = ['arg1']
    varargs = None
    varkw = None
    defaults = None
    kwonly = ['key1', 'key2']
    kwonly_defaults = []
    takes_context = False
    name = 'test_tag'
    
    args, kwargs = parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)

    assert args == [parser.compile_filter('arg1')]
    assert kwargs == {'key1': 'value1', 'key2': 'value2'}

def test_parse_bits_unexpected_keyword_argument():
    parser = Node()
    bits = ['arg1', 'unexpected=value']
    params = ['arg1']
    varargs = None
    varkw = None
    defaults = None
    kwonly = []
    kwonly_defaults = []
    takes_context = False
    name = 'test_tag'

    with pytest.raises(TemplateSyntaxError, match="received unexpected keyword argument"):
        parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)

def test_parse_bits_positional_after_keyword():
    parser = Node()
    bits = ['key=value', 'arg1']
    params = ['arg1']
    varargs = None
    varkw = None
    defaults = None
    kwonly = []
    kwonly_defaults = []
    takes_context = False
    name = 'test_tag'

    with pytest.raises(TemplateSyntaxError, match="received some positional argument\(s\) after some keyword argument\(s\)"):
        parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)

def test_parse_bits_too_many_positional_arguments():
    parser = Node()
    bits = ['arg1', 'arg2', 'arg3']
    params = ['arg1', 'arg2']
    varargs = None
    varkw = None
    defaults = None
    kwonly = []
    kwonly_defaults = []
    takes_context = False
    name = 'test_tag'

    with pytest.raises(TemplateSyntaxError, match="received too many positional arguments"):
        parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)

def test_parse_bits_missing_arguments():
    parser = Node()
    bits = ['arg1']
    params = ['arg1', 'arg2']
    varargs = None
    varkw = None
    defaults = None
    kwonly = []
    kwonly_defaults = []
    takes_context = False
    name = 'test_tag'

    with pytest.raises(TemplateSyntaxError, match="did not receive value\(s\) for the argument\(s\): 'arg2'"):
        parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)