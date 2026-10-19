import pytest
import os
from django.views.debug import ExceptionReporter

def create_test_file(filename, content):
    with open(filename, 'w') as f:
        f.write(content)

def test_get_lines_from_file():
    test_filename = 'test_source.py'
    test_content = """# coding=utf-8
def sample_function():
    print("Hello, World!")
    return True
"""
    create_test_file(test_filename, test_content)

    reporter = ExceptionReporter(None, None, None, None, False)

    # Test normal case
    lower_bound, pre_context, context_line, post_context = reporter._get_lines_from_file(
        test_filename, 1, 1)

    assert lower_bound == 0
    assert pre_context == []
    assert context_line == '    print("Hello, World!")'
    assert post_context == ['    return True']

    # Test when lineno is at the start
    lower_bound, pre_context, context_line, post_context = reporter._get_lines_from_file(
        test_filename, 0, 1)

    assert lower_bound == 0
    assert pre_context == []
    assert context_line == '# coding=utf-8'
    assert post_context == ['def sample_function():']

    # Test when lineno is at the end
    lower_bound, pre_context, context_line, post_context = reporter._get_lines_from_file(
        test_filename, 2, 1)

    assert lower_bound == 1
    assert pre_context == ['    print("Hello, World!")']
    assert context_line == '    return True'
    assert post_context == []

    # Test out-of-bounds lineno
    lower_bound, pre_context, context_line, post_context = reporter._get_lines_from_file(
        test_filename, 3, 1)

    assert lower_bound is None
    assert pre_context == []
    assert context_line is None
    assert post_context == []

    os.remove(test_filename)