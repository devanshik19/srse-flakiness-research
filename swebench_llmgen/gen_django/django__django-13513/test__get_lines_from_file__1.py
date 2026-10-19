import pytest
import os
from django.views.debug import ExceptionReporter

@pytest.fixture
def create_test_file():
    filename = 'test_file.py'
    with open(filename, 'w') as f:
        f.write("""# Sample Python file
def sample_function():
    return "Hello, World!"

# Example function
def another_function():
    pass
""")
    yield filename
    os.remove(filename)

def test_get_lines_from_file(create_test_file):
    filename = create_test_file
    reporter = ExceptionReporter(None, None, None, None, False)
    
    # Test with context lines in range
    lower_bound, pre_context, context_line, post_context = reporter._get_lines_from_file(filename, 1, 1)

    assert lower_bound == 0
    assert pre_context == ['# Sample Python file\n']
    assert context_line == 'def sample_function():\n'
    assert post_context == ['    return "Hello, World!"\n']

    # Test with lower bound exceeding file length
    lower_bound, pre_context, context_line, post_context = reporter._get_lines_from_file(filename, 0, 2)
    assert lower_bound == 0
    assert pre_context == []
    assert context_line == '# Sample Python file\n'
    assert post_context == ['def sample_function():\n', '    return "Hello, World!"\n']

    # Test with invalid line number
    lower_bound, pre_context, context_line, post_context = reporter._get_lines_from_file(filename, 10, 2)
    assert lower_bound is None
    assert pre_context == []
    assert context_line is None
    assert post_context == []
    
    # Test with file not found (simulate by passing non-existing file)
    lower_bound, pre_context, context_line, post_context = reporter._get_lines_from_file('non_existent_file.py', 0, 1)
    assert lower_bound is None
    assert pre_context == []
    assert context_line is None
    assert post_context == []