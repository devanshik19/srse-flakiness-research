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
        self.default_template = None
        self.max_post_process_passes = 2
        self._patterns = ['*.css', '*.js']
        self.hashed_files = {}

    def file_hash(self, name, content):
        return hashlib.md5(content.encode()).hexdigest()

    def hashed_name(self, name, content, filename):
        return f"{name}.{self.file_hash(name, content)}"

    def post_process(self, paths, dry_run=False, **options):
        if dry_run:
            return

        hashed_files = {}
        adjustable_paths = [path for path in paths if matches_patterns(path, self._patterns)]
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
        for path in paths:
            content = paths[path]
            hashed_name = self.hashed_name(path, content, path)
            hashed_files[path] = hashed_name
            yield path, hashed_name, True, False  # Simulating processed files


def test_post_process():
    mixin = HashedFilesMixin()
    test_paths = {
        'static/css/styles.css': 'body { color: red; }',
        'static/js/scripts.js': 'console.log("Hello, world!");',
    }

    # Test dry_run behavior
    result = list(mixin.post_process(test_paths, dry_run=True))
    assert result == []

    # Test regular post_process behavior
    processed_result = list(mixin.post_process(test_paths))
    assert len(processed_result) == 2
    assert 'static/css/styles.css' in mixin.hashed_files
    assert 'static/js/scripts.js' in mixin.hashed_files
    
    # Check hashed names
    for name, hashed_name, processed in processed_result:
        assert hashed_name == mixin.hashed_name(name, test_paths[name], name)
        assert processed is True

    # Test multiple passes
    mixin.max_post_process_passes = 1
    processed_result = list(mixin.post_process(test_paths))
    assert len(processed_result) == 2
    assert all(processed for _, _, processed in processed_result)

    # Check if oversubstitution error occurs
    mixin.max_post_process_passes = 1
    mixin._post_process = lambda paths, adjustable_paths, hashed_files: [(path, hashed_files[path], False, True) for path in paths]
    oversub_result = list(mixin.post_process(test_paths))
    assert len(oversub_result) == 3
    assert oversub_result[-1][2] == RuntimeError('Max post-process passes exceeded.')