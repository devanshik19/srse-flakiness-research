import hashlib
import json
import os
import posixpath
import re
from urllib.parse import unquote, urldefrag, urlsplit, urlunsplit
from django.conf import settings
from django.contrib.staticfiles.utils import check_settings, matches_patterns
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage, get_storage_class
from django.utils.functional import LazyObject
from django.contrib.auth.models import User
import pytest

class HashedFilesMixin:
    def __init__(self):
        self.max_post_process_passes = 2
        self._patterns = ['*.css', '*.js']
        self.hashed_files = {}

    def post_process(self, paths, dry_run=False, **options):
        if dry_run:
            return

        hashed_files = {}
        adjustable_paths = [
            path for path in paths
            if matches_patterns(path, self._patterns)
        ]
        for name, hashed_name, processed, _ in self._post_process(paths, adjustable_paths, hashed_files):
            yield name, hashed_name, processed

        paths = {path: paths[path] for path in adjustable_paths}

        for i in range(self.max_post_process_passes):
            substitutions = False
            for name, hashed_name, processed, subst in self._post_process(paths, adjustable_paths, hashed_files):
                yield name, hashed_name, processed
                substitutions = substitutions or subst

            if not substitutions:
                break

        if substitutions:
            yield 'All', None, RuntimeError('Max post-process passes exceeded.')

        self.hashed_files.update(hashed_files)

    def _post_process(self, paths, adjustable_paths, hashed_files):
        # Placeholder logic for testing
        for path in adjustable_paths:
            content = paths[path]
            hashed_name = self.hashed_name(path, content, 'filename')
            hashed_files[hashed_name] = content
            yield path, hashed_name, True, False

    def hashed_name(self, name, content, filename):
        return f"{name}.hashed"

@pytest.mark.parametrize("dry_run, expected_output", [
    (False, [('file1.js', 'file1.js.hashed', True), ('file2.css', 'file2.css.hashed', True)]),
    (True, [])
])
def test_post_process(dry_run, expected_output):
    mixin = HashedFilesMixin()
    paths = {
        'file1.js': 'console.log("Hello World");',
        'file2.css': 'body { background: #fff; }',
    }

    result = list(mixin.post_process(paths, dry_run=dry_run))
    assert result == expected_output