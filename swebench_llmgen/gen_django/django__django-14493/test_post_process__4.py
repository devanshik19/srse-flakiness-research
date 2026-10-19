import pytest
from django.contrib.staticfiles.storage import HashedFilesMixin
from django.contrib.auth.models import User
from collections import defaultdict

class TestHashedFilesMixin(HashedFilesMixin):
    def __init__(self):
        self.max_post_process_passes = 1
        self.patterns = []
        self.hashed_files = defaultdict(str)
    
    def _post_process(self, paths, adjustable_paths, hashed_files):
        # Mocking post process behavior for test
        for path in adjustable_paths:
            # Simulating the hashing of file names
            hashed_name = f"{path}.hashed"
            hashed_files[path] = hashed_name
            yield path, hashed_name, 'Processed', True

def test_post_process():
    mixin = TestHashedFilesMixin()
    
    # Prepare test data
    paths = {
        'file1.txt': 'content1',
        'file2.txt': 'content2',
        'file3.txt': 'content3',
    }
    adjustable_patterns = [r'.*\.txt$']  # Regex patterns for matching
    mixin._patterns = adjustable_patterns
    
    # Collect results from post_process
    results = list(mixin.post_process(paths))
    
    # Assert the functionality
    expected_results = [
        ('file1.txt', 'file1.txt.hashed', 'Processed'),
        ('file2.txt', 'file2.txt.hashed', 'Processed'),
        ('file3.txt', 'file3.txt.hashed', 'Processed')
    ]
    
    assert len(results) == 3
    assert all(result in expected_results for result in results)
    assert mixin.hashed_files['file1.txt'] == 'file1.txt.hashed'
    assert mixin.hashed_files['file2.txt'] == 'file2.txt.hashed'
    assert mixin.hashed_files['file3.txt'] == 'file3.txt.hashed'
    
def test_post_process_dry_run():
    mixin = TestHashedFilesMixin()
    
    # Test dry run mode
    paths = {
        'file4.txt': 'content4',
        'file5.txt': 'content5',
    }
    
    results = list(mixin.post_process(paths, dry_run=True))
    
    assert results == []