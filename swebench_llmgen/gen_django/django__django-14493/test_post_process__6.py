import pytest
from django.contrib.staticfiles.storage import HashedFilesMixin

class TestHashedFilesMixin(HashedFilesMixin):
    # Minimal implementation to test post_process
    _patterns = ['*.css', '*.js']
    
    def _post_process(self, paths, adjustable_paths, hashed_files):
        for path in adjustable_paths:
            hashed_name = f"{path}.hashed"  # Simulating a hashed name
            processed = True  # Simulating successful processing
            yield path, hashed_name, processed, False

    def __init__(self):
        self.hashed_files = {}
        self.max_post_process_passes = 3

@pytest.fixture
def mixin():
    return TestHashedFilesMixin()

def test_post_process_dry_run(mixin):
    paths = {'style.css': 'content', 'script.js': 'content'}
    result = list(mixin.post_process(paths, dry_run=True))
    assert result == []

def test_post_process(mixin):
    paths = {'style.css': 'content', 'script.js': 'content'}
    result = list(mixin.post_process(paths))
    expected_result = [
        ('style.css', 'style.css.hashed', True),
        ('script.js', 'script.js.hashed', True)
    ]
    assert result == expected_result
    assert mixin.hashed_files == {'style.css': 'style.css.hashed', 'script.js': 'script.js.hashed'}

def test_post_process_with_multiple_passes(mixin):
    mixin.max_post_process_passes = 1  # Limit to 1 pass for testing
    paths = {'style.css': 'content', 'script.js': 'content'}
    
    # Simulate additional behavior for adjustable paths
    def _post_process(paths, adjustable_paths, hashed_files):
        for path in adjustable_paths:
            if path == 'script.js':
                hashed_name = f"{path}.hashed"  # Successful processing
                processed = True
                yield path, hashed_name, processed, True  # Indicate that substitution occurred
            else:
                yield path, None, RuntimeError('Processing failure'), False  # Simulate a failure for style.css

    mixin._post_process = _post_process.__get__(mixin)  # Bind the new _post_process to `mixin`

    result = list(mixin.post_process(paths))
    expected_result = [
        ('style.css', None, RuntimeError('Processing failure')),
        ('script.js', 'script.js.hashed', True)
    ]
    assert result == expected_result
    assert mixin.hashed_files == {}