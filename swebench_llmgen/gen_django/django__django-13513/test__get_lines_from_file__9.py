import pytest
import os
import tempfile
from django.views.debug import ExceptionReporter

@pytest.fixture
def temp_file():
    # Create a temporary file with some content for testing
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, 'w') as f:
        f.write('Line 0\nLine 1\nLine 2\nLine 3\nLine 4\nLine 5\nLine 6\nLine 7\n')
    yield path
    os.remove(path)

def test_get_lines_from_file_within_bounds(temp_file):
    reporter = ExceptionReporter(None, None, None, None, None)
    lower, pre, context, post = reporter._get_lines_from_file(temp_file, 3, 2)

    assert lower == 1
    assert pre == ['Line 1', 'Line 2']
    assert context == 'Line 3'
    assert post == ['Line 4', 'Line 5']

def test_get_lines_from_file_upper_bound(temp_file):
    reporter = ExceptionReporter(None, None, None, None, None)
    lower, pre, context, post = reporter._get_lines_from_file(temp_file, 6, 2)

    assert lower == 4
    assert pre == ['Line 4', 'Line 5']
    assert context == 'Line 6'
    assert post == []

def test_get_lines_from_file_no_context(temp_file):
    reporter = ExceptionReporter(None, None, None, None, None)
    lower, pre, context, post = reporter._get_lines_from_file(temp_file, 0, 2)

    assert lower == 0
    assert pre == []
    assert context == 'Line 0'
    assert post == ['Line 1', 'Line 2']

def test_get_lines_from_file_out_of_bounds(temp_file):
    reporter = ExceptionReporter(None, None, None, None, None)
    lower, pre, context, post = reporter._get_lines_from_file(temp_file, 10, 2)

    assert lower is None
    assert pre == []
    assert context is None
    assert post == []

def test_get_lines_from_file_no_file():
    reporter = ExceptionReporter(None, None, None, None, None)
    lower, pre, context, post = reporter._get_lines_from_file('non_existent_file.py', 0, 2)

    assert lower is None
    assert pre == []
    assert context is None
    assert post == []