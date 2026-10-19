import pytest
import os
import tempfile
from django.views.debug import ExceptionReporter

@pytest.fixture
def create_temp_file():
    # Create a temporary file with sample content
    temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8')
    temp_file.write("Line 1\nLine 2\nLine 3\nLine 4\nLine 5\n")
    temp_file.close()
    yield temp_file.name
    os.remove(temp_file.name)

def test_get_lines_from_file(create_temp_file):
    reporter = ExceptionReporter(None, None, None, None, None)

    filename = create_temp_file
    lineno = 2
    context_lines = 1

    lower_bound, pre_context, context_line, post_context = reporter._get_lines_from_file(
        filename, lineno, context_lines
    )

    assert lower_bound == 1
    assert pre_context == ["Line 1\n"]
    assert context_line == "Line 2\n"
    assert post_context == ["Line 3\n"]

def test_get_lines_from_file_out_of_bounds(create_temp_file):
    reporter = ExceptionReporter(None, None, None, None, None)

    filename = create_temp_file
    lineno = 10  # Out of bounds
    context_lines = 1

    lower_bound, pre_context, context_line, post_context = reporter._get_lines_from_file(
        filename, lineno, context_lines
    )

    assert lower_bound is None
    assert pre_context == []
    assert context_line is None
    assert post_context == []

def test_get_lines_from_file_no_file():
    reporter = ExceptionReporter(None, None, None, None, None)

    filename = "non_existent_file.py"
    lineno = 2
    context_lines = 1

    lower_bound, pre_context, context_line, post_context = reporter._get_lines_from_file(
        filename, lineno, context_lines
    )

    assert lower_bound is None
    assert pre_context == []
    assert context_line is None
    assert post_context == []