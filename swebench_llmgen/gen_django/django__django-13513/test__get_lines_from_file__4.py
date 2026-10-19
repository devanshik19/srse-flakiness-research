import pytest
import tempfile
import os
from django.views.debug import ExceptionReporter

@pytest.fixture
def sample_file():
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(b'# Sample Python file\n')
        tmp_file.write(b'def sample_function():\n')
        tmp_file.write(b'    return "Hello, World!"\n')
        tmp_file.write(b'print(sample_function())\n')
        yield tmp_file.name
    os.remove(tmp_file.name)

def test_get_lines_from_file(sample_file):
    reporter = ExceptionReporter(None, None, None, None, False)
    
    # Test valid input
    lower_bound, pre_context, context_line, post_context = reporter._get_lines_from_file(
        sample_file, 2, 1
    )
    
    assert lower_bound == 1
    assert pre_context == [b'def sample_function():\n']
    assert context_line == b'    return "Hello, World!"\n'
    assert post_context == [b'print(sample_function())\n']
    
    # Test out of range line number
    lower_bound, pre_context, context_line, post_context = reporter._get_lines_from_file(
        sample_file, 10, 1
    )
    
    assert lower_bound is None
    assert pre_context == []
    assert context_line is None
    assert post_context == []

    # Test encoding detection
    with tempfile.NamedTemporaryFile(delete=False, mode='wb') as encoded_file:
        encoded_file.write(b'# -*- coding: utf-8 -*-\n')
        encoded_file.write(b'def test_func():\n')
        encoded_file.write(b'    return "Test"\n')
        encoded_file.write(b'test_func()\n')
        encoded_file_name = encoded_file.name
        
    lower_bound, pre_context, context_line, post_context = reporter._get_lines_from_file(
        encoded_file_name, 2, 1
    )
    
    assert lower_bound == 1
    assert pre_context == [b'def test_func():\n']
    assert context_line == b'    return "Test"\n'
    assert post_context == [b'test_func()\n']
    
    os.remove(encoded_file_name)