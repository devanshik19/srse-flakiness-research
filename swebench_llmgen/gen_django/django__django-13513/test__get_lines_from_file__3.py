import pytest
import os
from django.contrib.auth.models import User
from django.views.debug import ExceptionReporter

class TestExceptionReporter:

    def setup_method(self):
        # Create a temporary file for testing
        self.temp_file_path = 'test_file.py'
        self.context_lines = 2
        self.line_number = 3
        
        # Write test source code to the temporary file
        with open(self.temp_file_path, 'w') as f:
            f.write("# Sample Python file\n")
            f.write("def sample_function():\n")
            f.write("    return 'Hello World'\n")
            f.write("print(sample_function())\n")
            f.write("print('Done')\n")

    def teardown_method(self):
        # Remove the temporary file after tests
        if os.path.exists(self.temp_file_path):
            os.remove(self.temp_file_path)

    def test_get_lines_from_file_valid(self):
        reporter = ExceptionReporter(request=None, exc_type=None, exc_value=None, tb=None, is_email=False)
        lower_bound, pre_context, context_line, post_context = reporter._get_lines_from_file(
            self.temp_file_path, self.line_number, self.context_lines
        )

        assert lower_bound == 1
        assert pre_context == ["    return 'Hello World'\n", "print(sample_function())\n"]
        assert context_line == "print(sample_function())\n"
        assert post_context == ["print('Done')\n"]

    def test_get_lines_from_file_invalid_line(self):
        reporter = ExceptionReporter(request=None, exc_type=None, exc_value=None, tb=None, is_email=False)
        lower_bound, pre_context, context_line, post_context = reporter._get_lines_from_file(
            self.temp_file_path, 10, self.context_lines  # Line number beyond file length
        )

        assert lower_bound is None
        assert pre_context == []
        assert context_line is None
        assert post_context == []

    def test_get_lines_from_file_no_source(self):
        reporter = ExceptionReporter(request=None, exc_type=None, exc_value=None, tb=None, is_email=False)
        lower_bound, pre_context, context_line, post_context = reporter._get_lines_from_file(
            'non_existent_file.py', self.line_number, self.context_lines
        )

        assert lower_bound is None
        assert pre_context == []
        assert context_line is None
        assert post_context == []