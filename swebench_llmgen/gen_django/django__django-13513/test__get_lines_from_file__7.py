import functools
import re
import sys
import types
import warnings
from pathlib import Path
from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.template import Context, Engine, TemplateDoesNotExist
from django.template.defaultfilters import pprint
from django.urls import resolve
from django.utils import timezone
from django.utils.datastructures import MultiValueDict
from django.utils.encoding import force_str
from django.utils.module_loading import import_string
from django.utils.regex_helper import _lazy_re_compile
from django.utils.version import get_docs_version
import pytest
import traceback

from django.contrib.auth.models import User
from django.views.debug import ExceptionReporter

def test_get_lines_from_file():
    # Setup
    reporter = ExceptionReporter(None, None, None, None, False)
    test_file = Path(__file__).parent / "test_file.py"
    
    # Create a test file with some content
    with open(test_file, 'w') as f:
        f.write("# Test File\n")
        f.write("def test_function():\n")
        f.write("    return 'Hello World'\n")
        f.write("print(test_function())\n")

    # Valid case, with surrounding context
    lower_bound, pre_context, context_line, post_context = reporter._get_lines_from_file(test_file, 2, 1)
    assert lower_bound == 1
    assert pre_context == ["# Test File\n"]
    assert context_line == "    return 'Hello World'\n"
    assert post_context == ["print(test_function())\n"]

    # Edge case, requesting line above the first line
    lower_bound, pre_context, context_line, post_context = reporter._get_lines_from_file(test_file, 0, 1)
    assert lower_bound is None
    assert pre_context == []
    assert context_line is None
    assert post_context == ["# Test File\n"]

    # Edge case, requesting line below the last line
    lower_bound, pre_context, context_line, post_context = reporter._get_lines_from_file(test_file, 3, 1)
    assert lower_bound == 2
    assert pre_context == ["    return 'Hello World'\n"]
    assert context_line == "print(test_function())\n"
    assert post_context == []

    # Invalid case, file does not exist
    lower_bound, pre_context, context_line, post_context = reporter._get_lines_from_file("non_existent_file.py", 0, 1)
    assert lower_bound is None
    assert pre_context == []
    assert context_line is None
    assert post_context == []

    # Cleanup
    test_file.unlink()