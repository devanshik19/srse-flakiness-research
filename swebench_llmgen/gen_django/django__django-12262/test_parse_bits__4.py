import pytest
from django.template.library import parse_bits
from django.template.exceptions import TemplateSyntaxError
from django.utils.html import conditional_escape

class DummyParser:
    def compile_filter(self, bit):
        return bit

def test_parse_bits_valid_positional():
    parser = DummyParser()
    bits = ['arg1', 'arg2']
    params = ['arg1', 'arg2']
    varargs = None
    varkw = None
    defaults = None
    kwonly = []
    kwonly_defaults = []
    takes_context = False
    name = 'dummy_tag'

    args, kwargs = parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)

    assert args == ['arg1', 'arg2']
    assert kwargs == {}

def test_parse_bits_valid_keyword():
    parser = DummyParser()
    bits = ['arg1', {'kwarg1': 'value1'}]
    params = ['arg1']
    varargs = None
    varkw = None
    defaults = None
    kwonly = ['kwarg1']
    kwonly_defaults = []
    takes_context = False
    name = 'dummy_tag'

    args, kwargs = parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)

    assert args == ['arg1']
    assert kwargs == {'kwarg1': 'value1'}

def test_parse_bits_unexpected_keyword():
    parser = DummyParser()
    bits = ['arg1', {'unexpected_kwarg': 'value1'}]
    params = ['arg1']
    varargs = None
    varkw = None
    defaults = None
    kwonly = []
    kwonly_defaults = []
    takes_context = False
    name = 'dummy_tag'

    with pytest.raises(TemplateSyntaxError, match="received unexpected keyword argument 'unexpected_kwarg'"):
        parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)

def test_parse_bits_multiple_values_for_keyword():
    parser = DummyParser()
    bits = ['arg1', {'kwarg1': 'value1'}, {'kwarg1': 'value2'}]
    params = ['arg1']
    varargs = None
    varkw = None
    defaults = None
    kwonly = ['kwarg1']
    kwonly_defaults = []
    takes_context = False
    name = 'dummy_tag'

    with pytest.raises(TemplateSyntaxError, match="received multiple values for keyword argument 'kwarg1'"):
        parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)

def test_parse_bits_positional_after_keyword():
    parser = DummyParser()
    bits = [{'kwarg1': 'value1'}, 'arg2']
    params = ['arg1']
    varargs = None
    varkw = None
    defaults = None
    kwonly = []
    kwonly_defaults = []
    takes_context = False
    name = 'dummy_tag'

    with pytest.raises(TemplateSyntaxError, match="received some positional argument\(s\) after some keyword argument\(s\)"):
        parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)

def test_parse_bits_missing_positional_arguments():
    parser = DummyParser()
    bits = ['arg1']
    params = ['arg1', 'arg2']
    varargs = None
    varkw = None
    defaults = None
    kwonly = []
    kwonly_defaults = []
    takes_context = False
    name = 'dummy_tag'

    with pytest.raises(TemplateSyntaxError, match="did not receive value\(s\) for the argument\(s\): 'arg2'"):
        parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)