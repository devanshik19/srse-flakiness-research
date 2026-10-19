import pytest
from django.template.library import parse_bits
from django.template.exceptions import TemplateSyntaxError
from django.template import Engine

@pytest.mark.parametrize("bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name, expected_args, expected_kwargs", [
    (['arg1', 'arg2'], ['arg1', 'arg2'], None, None, None, [], [], False, 'simple_tag', ['arg1', 'arg2'], {}),
    (['arg1', 'key1=value1'], ['arg1'], None, None, None, ['key1'], [], False, 'simple_tag', ['arg1'], {'key1': 'value1'}),
    (['context', 'arg1'], ['context', 'arg1'], None, None, None, [], [], True, 'simple_tag', ['arg1'], {}),
    (['key1=value1', 'arg1'], ['arg1'], None, None, None, ['key1'], [], False, 'simple_tag', ['arg1'], {'key1': 'value1'}),
    (['arg1', 'arg2', 'key1=value1'], ['arg1', 'arg2'], None, None, None, ['key1'], [], False, 'simple_tag', ['arg1', 'arg2'], {'key1': 'value1'}),
])
def test_parse_bits_valid(bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name, expected_args, expected_kwargs):
    # Create a mock parser with required methods
    class MockParser:
        def compile_filter(self, bit):
            return bit
        
        def token_kwargs(self, bit_list, parser):
            if '=' in bit_list[0]:
                key, value = bit_list[0].split('=', 1)
                return {key: value}
            return {}

    parser = MockParser()
    args, kwargs = parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)
    
    assert args == expected_args
    assert kwargs == expected_kwargs

@pytest.mark.parametrize("bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name", [
    (['context'], ['context'], None, None, None, [], [], True, 'simple_tag'),  # Valid context usage
    (['context'], ['wrong'], None, None, None, [], [], True, 'simple_tag'),    # Invalid context
    (['arg1', 'key1=value1'], ['arg1'], None, None, None, [], [], False, 'simple_tag'),     # Valid kwarg
    (['arg1', 'arg2'], ['arg1'], None, None, None, [], [], False, 'simple_tag'),  # More positional args than expected
    (['key1=value1', 'key1=value2'], ['arg1'], None, None, None, ['key1'], [], False, 'simple_tag'),  # Duplicate kwarg
    (['arg1'], ['arg1'], None, None, None, ['key1'], [], False, 'simple_tag'),  # Missing required kwonly
    (['arg1', 'key1=value1', 'arg2'], ['arg1', 'arg2'], None, None, None, [], [], False, 'simple_tag'),  # Positional after kwarg
])
def test_parse_bits_invalid(bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name):
    class MockParser:
        def compile_filter(self, bit):
            return bit
        
        def token_kwargs(self, bit_list, parser):
            if '=' in bit_list[0]:
                key, value = bit_list[0].split('=')
                return {key: value}
            return {}

    parser = MockParser()
    
    with pytest.raises(TemplateSyntaxError):
        parse_bits(parser, bits, params, varargs, varkw, defaults, kwonly, kwonly_defaults, takes_context, name)