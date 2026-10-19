import os
import tempfile
import pytest
from django.views.debug import ExceptionReporter

@pytest.fixture
def create_temp_file():
    # Create a temporary file for testing
    fn = tempfile.NamedTemporaryFile(delete=False, mode='w+')
    fn.write("Line 1\nLine 2\nLine 3\nLine 4\nLine 5\n")
    fn.close()
    yield fn.name
    os.remove(fn.name)

def test_get_lines_from_file(create_temp_file):
    reporter = ExceptionReporter(None, None, None, None, False)
    filename = create_temp_file

    # Test with valid lineno and context_lines
    lineno = 2
    context_lines = 1
    lower_bound, pre_context, context_line, post_context = reporter._get_lines_from_file(filename, lineno, context_lines)

    assert lower_bound == 1
    assert pre_context == ["Line 1"]
    assert context_line == "Line 2\n"
    assert post_context == ["Line 3\n"]

    # Test with lineno at the beginning
    lineno = 0
    lower_bound, pre_context, context_line, post_context = reporter._get_lines_from_file(filename, lineno, context_lines)

    assert lower_bound == 0
    assert pre_context == []
    assert context_line == "Line 1\n"
    assert post_context == ["Line 2\n"]

    # Test with lineno at the end
    lineno = 4
    lower_bound, pre_context, context_line, post_context = reporter._get_lines_from_file(filename, lineno, context_lines)

    assert lower_bound == 3
    assert pre_context == ["Line 4\n"]
    assert context_line == "Line 5\n"
    assert post_context == []

    # Test with lineno out of bounds
    lineno = 10
    lower_bound, pre_context, context_line, post_context = reporter._get_lines_from_file(filename, lineno, context_lines)

    assert lower_bound is None
    assert pre_context == []
    assert context_line is None
    assert post_context == []