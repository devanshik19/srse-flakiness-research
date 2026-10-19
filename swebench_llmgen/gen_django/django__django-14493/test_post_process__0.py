import pytest
from django.contrib.staticfiles.storage import HashedFilesMixin
from django.contrib.auth.models import User

class TestHashedFilesMixin(HashedFilesMixin):
    def __init__(self):
        self.max_post_process_passes = 3
        self._patterns = [re.compile(r'.*')]
        self.hashed_files = {}

    def _post_process(self, paths, adjustable_paths, hashed_files):
        processed_results = []
        for path in adjustable_paths:
            # Simulating some hashing logic for testing purposes
            content = paths[path]
            hashed_name = f"{path}.hashed"  # Example of a hashed name
            processed_results.append((path, hashed_name, content, True))
        return processed_results

def test_post_process_with_dry_run():
    mixin = TestHashedFilesMixin()
    paths = {'file1.txt': 'content1', 'file2.txt': 'content2'}

    results = list(mixin.post_process(paths, dry_run=True))
    assert results == []

def test_post_process_without_adjustable_files():
    mixin = TestHashedFilesMixin()
    paths = {'file1.txt': 'content1', 'file2.txt': 'content2'}
    
    mixin._patterns = []  # No patterns to match
    results = list(mixin.post_process(paths))
    
    assert len(results) == 0
    assert mixin.hashed_files == {}

def test_post_process_with_adjustable_files():
    mixin = TestHashedFilesMixin()
    paths = {'file1.txt': 'content1', 'file2.txt': 'content2'}
    
    results = list(mixin.post_process(paths))
    
    assert len(results) == 2
    assert mixin.hashed_files == {'file1.txt': 'content1', 'file2.txt': 'content2'}
    assert results[0] == ('file1.txt', 'file1.txt.hashed', 'content1')
    assert results[1] == ('file2.txt', 'file2.txt.hashed', 'content2')

def test_post_process_exceeding_max_passes():
    mixin = TestHashedFilesMixin()
    mixin.max_post_process_passes = 1  # Set to 1 for testing
    paths = {'file1.txt': 'content1', 'file2.txt': 'content2'}

    mixin._patterns = [re.compile(r'.*')]  # Conditions for adjustable files
    results = list(mixin.post_process(paths))

    assert results[-1] == ('All', None, RuntimeError('Max post-process passes exceeded.'))