import pytest
from django.template.library import parse_bits
from django.template.exceptions import TemplateSyntaxError
from unittest.mock import Mock

def test_parse_bits_no_context():
    parser = Mock()
    bits = ['arg1', 'arg2']
    params = ['param1', 'param2']
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

def test_parse_bits_with_context_correct_usage():
    parser = Mock()
    bits = ['context', 'arg1', 'arg2']
    params = ['context', 'param1', 'param2']
    varargs = None
    varkw = None
    defaults = None
    kwonly = []
    kwonly_defaults = []
    takes_context = True
    name = 'test_tag'

    args, kwargs = parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)

    assert args == [parser.compile_filter('arg1'), parser.compile_filter('arg2')]
    assert kwargs == {}

def test_parse_bits_with_context_missing_context():
    parser = Mock()
    bits = ['arg1', 'arg2']
    params = ['param1', 'param2']
    varargs = None
    varkw = None
    defaults = None
    kwonly = []
    kwonly_defaults = []
    takes_context = True
    name = 'test_tag'

    with pytest.raises(TemplateSyntaxError):
        parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)

def test_parse_bits_unexpected_kwarg():
    parser = Mock()
    bits = ['arg1', 'arg2']
    params = ['param1']
    varargs = None
    varkw = None
    defaults = None
    kwonly = []
    kwonly_defaults = []
    takes_context = False
    name = 'test_tag'

    with pytest.raises(TemplateSyntaxError):
        parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)

def test_parse_bits_multiple_values_for_kwarg():
    parser = Mock()
    bits = ['arg1', 'arg2', 'param1=value1', 'param1=value2']
    params = ['param1']
    varargs = None
    varkw = None
    defaults = None
    kwonly = []
    kwonly_defaults = []
    takes_context = False
    name = 'test_tag'

    with pytest.raises(TemplateSyntaxError):
        parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)

def test_parse_bits_positional_after_kwarg():
    parser = Mock()
    bits = ['param1=value1', 'arg1', 'arg2']
    params = ['param1']
    varargs = None
    varkw = None
    defaults = None
    kwonly = []
    kwonly_defaults = []
    takes_context = False
    name = 'test_tag'

    with pytest.raises(TemplateSyntaxError):
        parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)

def test_parse_bits_too_many_positional_arguments():
    parser = Mock()
    bits = ['arg1', 'arg2', 'arg3']
    params = ['param1', 'param2']
    varargs = None
    varkw = None
    defaults = None
    kwonly = []
    kwonly_defaults = []
    takes_context = False
    name = 'test_tag'

    with pytest.raises(TemplateSyntaxError):
        parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)

def test_parse_bits_unhandled_params_and_kwargs():
    parser = Mock()
    bits = ['arg1']
    params = ['param1', 'param2']
    varargs = None
    varkw = None
    defaults = None
    kwonly = ['kwarg1']
    kwonly_defaults = []
    takes_context = False
    name = 'test_tag'

    with pytest.raises(TemplateSyntaxError):
        parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)