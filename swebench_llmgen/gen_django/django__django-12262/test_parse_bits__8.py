import pytest
from django.template.library import parse_bits
from django.template.exceptions import TemplateSyntaxError
from django.template import Template, Engine

# Sample parser class to simulate the required parser behavior
class FakeParser:
    def compile_filter(self, bit):
        return bit  # Simulate returning the bit as a filtered output

# Dummy function to act as the token_kwargs simulating the expected behavior.
def token_kwargs(bits, parser):
    kwargs = {}
    for bit in bits:
        if '=' in bit:
            key, value = bit.split('=', 1)
            kwargs[key.strip()] = value.strip()
    return kwargs

@pytest.fixture
def parser():
    return FakeParser()

def test_parse_bits_positional_arguments(parser):
    bits = ['arg1', 'arg2']
    params = ['arg1', 'arg2']
    args, kwargs = parse_bits(parser, bits, params, None, None, None, [], [], False, 'test_tag')
    assert args == ['arg1', 'arg2']
    assert kwargs == {}

def test_parse_bits_with_keyword_arguments(parser):
    bits = ['arg1', 'arg2=value2']
    params = ['arg1', 'arg2']
    args, kwargs = parse_bits(parser, bits, params, None, None, None, [], [], False, 'test_tag')
    assert args == ['arg1']
    assert kwargs == {'arg2': 'value2'}

def test_parse_bits_unexpected_keyword_argument(parser):
    bits = ['arg1', 'invalid_arg=value']
    params = ['arg1']
    with pytest.raises(TemplateSyntaxError) as excinfo:
        parse_bits(parser, bits, params, None, None, None, [], [], False, 'test_tag')
    assert "'test_tag' received unexpected keyword argument 'invalid_arg'" in str(excinfo.value)

def test_parse_bits_multiple_keyword_arguments(parser):
    bits = ['arg1', 'arg1=value1', 'arg2=value2']
    params = ['arg1', 'arg2']
    with pytest.raises(TemplateSyntaxError) as excinfo:
        parse_bits(parser, bits, params, None, None, None, [], [], False, 'test_tag')
    assert "'test_tag' received multiple values for keyword argument 'arg1'" in str(excinfo.value)

def test_parse_bits_keyword_after_positional(parser):
    bits = ['arg1', 'arg2=value2', 'arg3']
    params = ['arg1', 'arg2', 'arg3']
    with pytest.raises(TemplateSyntaxError) as excinfo:
        parse_bits(parser, bits, params, None, None, None, [], [], False, 'test_tag')
    assert "'test_tag' received some positional argument(s) after some keyword argument(s)" in str(excinfo.value)

def test_parse_bits_missing_arguments(parser):
    bits = ['arg1']
    params = ['arg1', 'arg2']
    with pytest.raises(TemplateSyntaxError) as excinfo:
        parse_bits(parser, bits, params, None, None, None, [], [], False, 'test_tag')
    assert "'test_tag' did not receive value(s) for the argument(s): 'arg2'" in str(excinfo.value)