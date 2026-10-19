import pytest
import tempfile
from django.views.debug import ExceptionReporter

@pytest.fixture
def create_temp_file():
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(b'# coding: utf-8\n')
        temp_file.write(b'line 1\n')
        temp_file.write(b'line 2\n')
        temp_file.write(b'line 3\n')
        temp_file.write(b'line 4\n')
        temp_file.write(b'line 5\n')
        yield temp_file.name

def test_get_lines_from_file(create_temp_file):
    reporter = ExceptionReporter(None, None, None, None, None)
    filename = create_temp_file

    # Test normal case
    lower_bound, pre_context, context_line, post_context = reporter._get_lines_from_file(filename, 2, 1)

    assert lower_bound == 1
    assert pre_context == [b'# coding: utf-8\n', b'line 1\n']
    assert context_line == b'line 2\n'
    assert post_context == [b'line 3\n']

    # Test with context_lines more than available lines above and below
    lower_bound, pre_context, context_line, post_context = reporter._get_lines_from_file(filename, 0, 10)

    assert lower_bound == 0
    assert pre_context == []
    assert context_line == b'line 1\n'
    assert post_context == [b'line 2\n', b'line 3\n', b'line 4\n', b'line 5\n']

    # Test with lineno out of range
    lower_bound, pre_context, context_line, post_context = reporter._get_lines_from_file(filename, 10, 1)

    assert lower_bound is None
    assert pre_context == []
    assert context_line is None
    assert post_context == []

    # Test with encoding detection
    with open(filename, 'rb') as f:
        f.write(b'\n# coding: ascii\nline a\nline b\nline c\n')
    
    lower_bound, pre_context, context_line, post_context = reporter._get_lines_from_file(filename, 1, 1)

    assert lower_bound == 0
    assert pre_context == []
    assert context_line == b'# coding: ascii\n'
    assert post_context == [b'line a\n']

    # Cleanup: Remove the temporary file
    import os
    os.remove(filename)