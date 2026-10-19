import pytest
from django.template.library import parse_bits
from django.template.exceptions import TemplateSyntaxError
from django.template import Context, Template


def dummy_parser():
    class DummyParser:
        def compile_filter(self, bit):
            return bit  # Simulate behavior of compiling filters

    return DummyParser()


def test_parse_bits_success():
    parser = dummy_parser()
    bits = ['arg1', 'arg2']

    # Case 1: No context, valid positional args
    args, kwargs = parse_bits(parser, bits, ['arg1', 'arg2'], None, None, None, None, None, False, "test_tag")
    assert args == ['arg1', 'arg2']
    assert kwargs == {}

    # Case 2: With context, valid context first, then positional args
    args, kwargs = parse_bits(parser, bits, ['context', 'arg1', 'arg2'], None, None, None, None, None, True, "test_tag")
    assert args == ['arg1', 'arg2']
    assert kwargs == {}


def test_parse_bits_error_unexpected_keyword():
    parser = dummy_parser()
    bits = ['arg1', 'arg2']

    with pytest.raises(TemplateSyntaxError) as excinfo:
        parse_bits(parser, bits, ['arg1', 'arg2'], None, None, None, None, None, False, "test_tag")
    
    assert "unexpected keyword argument" in str(excinfo.value)


def test_parse_bits_error_multiple_values():
    parser = dummy_parser()
    bits = ['arg1', 'arg2', 'arg1=value1']

    with pytest.raises(TemplateSyntaxError) as excinfo:
        parse_bits(parser, bits, ['arg1', 'arg2'], None, None, None, None, None, False, "test_tag")
    
    assert "multiple values for keyword argument" in str(excinfo.value)


def test_parse_bits_error_positional_after_keyword():
    parser = dummy_parser()
    bits = ['arg1=value1', 'arg2']

    with pytest.raises(TemplateSyntaxError) as excinfo:
        parse_bits(parser, bits, ['arg1', 'arg2'], None, None, None, None, None, False, "test_tag")
    
    assert "received some positional argument(s) after some keyword argument(s)" in str(excinfo.value)


def test_parse_bits_error_too_many_positional():
    parser = dummy_parser()
    bits = ['arg1', 'arg2', 'arg3']

    with pytest.raises(TemplateSyntaxError) as excinfo:
        parse_bits(parser, bits, ['arg1'], None, None, None, None, None, False, "test_tag")
    
    assert "received too many positional arguments" in str(excinfo.value)


def test_parse_bits_error_missing_arguments():
    parser = dummy_parser()
    bits = ['arg1']

    with pytest.raises(TemplateSyntaxError) as excinfo:
        parse_bits(parser, bits, ['arg1', 'arg2'], None, None, None, None, None, False, "test_tag")
    
    assert "did not receive value(s) for the argument(s): 'arg2'" in str(excinfo.value)