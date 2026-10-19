import pytest
from django.contrib.staticfiles.storage import HashedFilesMixin
from django.contrib.auth.models import User
from django.core.files.base import ContentFile

class TestHashedFilesMixin(HashedFilesMixin):
    def __init__(self):
        self.max_post_process_passes = 2
        self._patterns = ['*.css', '*.js']
        self.hashed_files = {}

    def _post_process(self, paths, adjustable_paths, hashed_files):
        results = []
        for path in paths:
            content = paths[path]
            hash_name = self.hashed_name(path, content, path)
            processed = True
            results.append((path, hash_name, processed, False))
        return results

    def hashed_name(self, name, content, filename):
        return f"{name}.hashed"

def test_post_process_with_dry_run():
    mixin = TestHashedFilesMixin()
    paths = {
        'static/file1.css': ContentFile(b'content1'),
        'static/file2.js': ContentFile(b'content2'),
    }
    result = list(mixin.post_process(paths, dry_run=True))
    assert result == []

def test_post_process_without_dry_run():
    mixin = TestHashedFilesMixin()
    paths = {
        'static/file1.css': ContentFile(b'content1'),
        'static/file2.js': ContentFile(b'content2'),
    }
    result = list(mixin.post_process(paths, dry_run=False))
    assert len(result) == 2
    assert result[0] == ('static/file1.css', 'static/file1.css.hashed', True)
    assert result[1] == ('static/file2.js', 'static/file2.js.hashed', True)

def test_post_process_with_adjustable_paths():
    mixin = TestHashedFilesMixin()
    paths = {
        'static/file1.css': ContentFile(b'content1'),
        'static/file2.js': ContentFile(b'content2'),
        'static/file3.png': ContentFile(b'content3'),
    }
    adjustable_paths = ['static/file1.css', 'static/file2.js']
    
    # Simulating the adjustable_paths effect in _post_process
    mixin._patterns = ['*.css']  # Only css files will be hashed
    result = list(mixin.post_process(paths, dry_run=False))
    assert len(result) == 2  # Only file1 and file2 should be processed.
    assert result[0] == ('static/file1.css', 'static/file1.css.hashed', True)
    assert result[1] == ('static/file2.js', 'static/file2.js.hashed', True)

def test_post_process_exceeds_max_passes():
    mixin = TestHashedFilesMixin()
    mixin.max_post_process_passes = 1  # Limit to one pass
    paths = {
        'static/file1.css': ContentFile(b'content1'),
    }
    
    result = list(mixin.post_process(paths, dry_run=False))
    assert len(result) == 1
    assert result[0] == ('All', None, RuntimeError('Max post-process passes exceeded.'))