import os
import pytest
from django.contrib.auth.models import User
from django.views.debug import ExceptionReporter

@pytest.fixture
def create_temp_file():
    filename = "temp_test_file.py"
    content = b"# Sample file\nprint('Hello, World!')\n# End of file"
    with open(filename, 'wb') as f:
        f.write(content)
    yield filename
    os.remove(filename)

def test_get_lines_from_file(create_temp_file):
    reporter = ExceptionReporter(None, None, None, None, False)
    filename = create_temp_file

    # Test normal case with context lines
    lower_bound, pre_context, context_line, post_context = reporter._get_lines_from_file(filename, 1, 1)
    assert lower_bound == 0
    assert pre_context == [b"# Sample file\n"]
    assert context_line == b"print('Hello, World!')\n"
    assert post_context == [b"# End of file"]

    # Test edge case with too few lines
    lower_bound, pre_context, context_line, post_context = reporter._get_lines_from_file(filename, 0, 1)
    assert lower_bound == 0
    assert pre_context == []
    assert context_line == b"# Sample file\n"
    assert post_context == [b"print('Hello, World!')\n"]

    # Test case with line number out of file bounds
    lower_bound, pre_context, context_line, post_context = reporter._get_lines_from_file(filename, 10, 1)
    assert lower_bound is None
    assert pre_context == []
    assert context_line is None
    assert post_context == []

    # Test with a non-existing file
    lower_bound, pre_context, context_line, post_context = reporter._get_lines_from_file("non_existing_file.py", 0, 1)
    assert lower_bound is None
    assert pre_context == []
    assert context_line is None
    assert post_context == []