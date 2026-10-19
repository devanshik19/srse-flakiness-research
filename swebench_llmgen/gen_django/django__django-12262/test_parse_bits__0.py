import pytest
from django.template.library import parse_bits
from django.template.exceptions import TemplateSyntaxError
from django.template import Template
from django.utils.html import conditional_escape


def test_parse_bits_valid_positional_arguments():
    parser = Template('').parser
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


def test_parse_bits_valid_keyword_arguments():
    parser = Template('').parser
    bits = ['arg1', 'keyword=val1']
    params = ['arg1']
    varargs = None
    varkw = None
    defaults = None
    kwonly = ['keyword']
    kwonly_defaults = []
    takes_context = False
    name = 'test_tag'
    
    args, kwargs = parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)
    
    assert args == [parser.compile_filter('arg1')]
    assert kwargs == {'keyword': 'val1'}


def test_parse_bits_multiple_keyword_arguments():
    parser = Template('').parser
    bits = ['arg1', 'keyword1=val1', 'keyword2=val2']
    params = ['arg1']
    varargs = None
    varkw = None
    defaults = None
    kwonly = ['keyword1', 'keyword2']
    kwonly_defaults = []
    takes_context = False
    name = 'test_tag'
    
    args, kwargs = parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)
    
    assert args == [parser.compile_filter('arg1')]
    assert kwargs == {'keyword1': 'val1', 'keyword2': 'val2'}


def test_parse_bits_unexpected_keyword_argument():
    parser = Template('').parser
    bits = ['arg1', 'unexpected=val']
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
        
    assert "'%s' received unexpected keyword argument 'unexpected'" % name in str(excinfo.value)


def test_parse_bits_multiple_values_for_keyword_argument():
    parser = Template('').parser
    bits = ['arg1', 'keyword=val1', 'keyword=val2']
    params = ['arg1']
    varargs = None
    varkw = None
    defaults = None
    kwonly = ['keyword']
    kwonly_defaults = []
    takes_context = False
    name = 'test_tag'
    
    with pytest.raises(TemplateSyntaxError) as excinfo:
        parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)
        
    assert "'%s' received multiple values for keyword argument 'keyword'" % name in str(excinfo.value)


def test_parse_bits_positional_after_keyword_arguments():
    parser = Template('').parser
    bits = ['keyword=val', 'arg1']
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


def test_parse_bits_missing_positional_arguments():
    parser = Template('').parser
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