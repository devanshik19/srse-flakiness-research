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
        self.hashed_files = {}
        self.max_post_process_passes = 2
        self._patterns = []
        
    def post_process(self, paths, dry_run=False, **options):
        if dry_run:
            return
        hashed_files = {}
        adjustable_paths = [
            path for path in paths
            if matches_patterns(path, self._patterns)
        ]
        processed_adjustable_paths = {}
        for name, hashed_name, processed, _ in self._post_process(paths, adjustable_paths, hashed_files):
            if name not in adjustable_paths or isinstance(processed, Exception):
                yield name, hashed_name, processed
            else:
                processed_adjustable_paths[name] = (name, hashed_name, processed)
        paths = {path: paths[path] for path in adjustable_paths}
        for i in range(self.max_post_process_passes):
            substitutions = False
            for name, hashed_name, processed, subst in self._post_process(paths, adjustable_paths, hashed_files):
                processed_adjustable_paths[name] = (name, hashed_name, processed)
                substitutions = substitutions or subst
            if not substitutions:
                break
        if substitutions:
            yield 'All', None, RuntimeError('Max post-process passes exceeded.')
        self.hashed_files.update(hashed_files)
        yield from processed_adjustable_paths.values()

    def _post_process(self, paths, adjustable_paths, hashed_files):
        # A mock implementation of _post_process to enable testing
        for path in adjustable_paths:
            # Simulating hashing and returning results
            hashed_name = f"{path}.hash"
            processed = paths[path]
            yield path, hashed_name, processed, False


@pytest.mark.parametrize("dry_run, expected_output", [
    (True, None),
    (False, [
        ('file1.txt', 'file1.txt.hash', 'content of file 1'),
        ('file2.txt', 'file2.txt.hash', 'content of file 2')
    ]),
])
def test_post_process(dry_run, expected_output):
    mixin = HashedFilesMixin()
    mixin._patterns = ['*.txt']
    paths = {
        'file1.txt': 'content of file 1',
        'file2.txt': 'content of file 2',
        'image.png': 'image content'
    }
    
    if dry_run:
        result = list(mixin.post_process(paths, dry_run=dry_run))
        assert result == expected_output
    else:
        result = list(mixin.post_process(paths, dry_run=dry_run))
        assert len(result) == 2
        assert result[0] == ('file1.txt', 'file1.txt.hash', 'content of file 1')
        assert result[1] == ('file2.txt', 'file2.txt.hash', 'content of file 2')
        assert 'image.png' not in mixin.hashed_files