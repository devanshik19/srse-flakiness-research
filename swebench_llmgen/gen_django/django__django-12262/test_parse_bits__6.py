import pytest
from django.template.library import parse_bits
from django.template.exceptions import TemplateSyntaxError
from django.template import TemplateSyntaxError, Context
from django.utils.html import conditional_escape

def dummy_parser():
    class Parser:
        def compile_filter(self, bit):
            return bit  # Just return the bit for testing purposes
    return Parser()

def test_parse_bits_valid_positional_arguments():
    parser = dummy_parser()
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

    assert args == ['arg1', 'arg2']
    assert kwargs == {}

def test_parse_bits_with_keyword_arguments():
    parser = dummy_parser()
    bits = ['arg1', 'arg2', 'kwarg1=value1']
    params = ['arg1', 'arg2']
    varargs = None
    varkw = None
    defaults = None
    kwonly = ['kwarg1']
    kwonly_defaults = []
    takes_context = False
    name = 'test_tag'

    args, kwargs = parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)

    assert args == ['arg1', 'arg2']
    assert kwargs == {'kwarg1': 'value1'}

def test_parse_bits_with_unexpected_keyword_argument():
    parser = dummy_parser()
    bits = ['arg1', 'bad_kwarg=value1']
    params = ['arg1']
    varargs = None
    varkw = None
    defaults = None
    kwonly = []
    kwonly_defaults = []
    takes_context = False
    name = 'test_tag'

    with pytest.raises(TemplateSyntaxError) as excinfo:
        parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)
    assert "'%s' received unexpected keyword argument" % name in str(excinfo.value)

def test_parse_bits_multiple_values_for_keyword_argument():
    parser = dummy_parser()
    bits = ['arg1', 'kwarg1=value1', 'kwarg1=value2']
    params = ['arg1']
    varargs = None
    varkw = None
    defaults = None
    kwonly = ['kwarg1']
    kwonly_defaults = []
    takes_context = False
    name = 'test_tag'

    with pytest.raises(TemplateSyntaxError) as excinfo:
        parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)
    assert "'%s' received multiple values for keyword argument" % name in str(excinfo.value)

def test_parse_bits_positional_after_keyword():
    parser = dummy_parser()
    bits = ['kwarg1=value1', 'arg1']
    params = ['arg1']
    varargs = None
    varkw = None
    defaults = None
    kwonly = []
    kwonly_defaults = []
    takes_context = False
    name = 'test_tag'

    with pytest.raises(TemplateSyntaxError) as excinfo:
        parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)
    assert "'%s' received some positional argument(s) after some keyword argument(s)" % name in str(excinfo.value)

def test_parse_bits_missing_arguments():
    parser = dummy_parser()
    bits = ['arg1']
    params = ['arg1', 'arg2']
    varargs = None
    varkw = None
    defaults = None
    kwonly = []
    kwonly_defaults = []
    takes_context = False
    name = 'test_tag'

    with pytest.raises(TemplateSyntaxError) as excinfo:
        parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)
    assert "'%s' did not receive value(s) for the argument(s): 'arg2'" % name in str(excinfo.value)