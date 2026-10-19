import pytest
from django.template.library import parse_bits
from django.template.exceptions import TemplateSyntaxError
from django.template import Template

def test_parse_bits_valid():
    parser = Template('foo %s' % ' '.join(['arg1', 'arg2']))
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

def test_parse_bits_with_kwarg():
    parser = Template('foo %s' % ' '.join(['arg1', 'arg2']))
    bits = ['arg1', 'arg2', 'key=value']
    params = ['arg1', 'arg2']
    varargs = None
    varkw = None
    defaults = None
    kwonly = ['key']
    kwonly_defaults = []
    takes_context = False
    name = 'test_tag'

    args, kwargs = parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)

    assert args == ['arg1', 'arg2']
    assert kwargs == {'key': 'value'}

def test_parse_bits_missing_context():
    parser = Template('foo %s' % ' '.join(['arg1', 'arg2']))
    bits = ['arg1', 'arg2']
    params = ['context', 'arg1', 'arg2']
    varargs = None
    varkw = None
    defaults = None
    kwonly = []
    kwonly_defaults = []
    takes_context = True
    name = 'test_tag'

    with pytest.raises(TemplateSyntaxError):
        parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)

def test_parse_bits_too_many_positional():
    parser = Template('foo %s' % ' '.join(['arg1', 'arg2']))
    bits = ['arg1', 'arg2', 'arg3']
    params = ['arg1', 'arg2']
    varargs = None
    varkw = None
    defaults = None
    kwonly = []
    kwonly_defaults = []
    takes_context = False
    name = 'test_tag'

    with pytest.raises(TemplateSyntaxError):
        parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)

def test_parse_bits_unexpected_kwarg():
    parser = Template('foo %s' % ' '.join(['arg1', 'arg2']))
    bits = ['arg1', 'arg2', 'unexpected_kwarg=value']
    params = ['arg1', 'arg2']
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
    parser = Template('foo %s' % ' '.join(['arg1', 'arg2']))
    bits = ['arg1', 'arg2', 'key=value1', 'key=value2']
    params = ['arg1', 'arg2']
    varargs = None
    varkw = None
    defaults = None
    kwonly = ['key']
    kwonly_defaults = []
    takes_context = False
    name = 'test_tag'

    with pytest.raises(TemplateSyntaxError):
        parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)

def test_parse_bits_positional_after_kwarg():
    parser = Template('foo %s' % ' '.join(['arg1', 'arg2']))
    bits = ['key=value', 'arg1', 'arg2']
    params = ['arg1', 'arg2']
    varargs = None
    varkw = None
    defaults = None
    kwonly = []
    kwonly_defaults = []
    takes_context = False
    name = 'test_tag'

    with pytest.raises(TemplateSyntaxError):
        parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)