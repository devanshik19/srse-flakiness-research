import pytest
from django.contrib.auth.models import User
from django.contrib.staticfiles.storage import HashedFilesMixin

class TestHashedFilesMixin(HashedFilesMixin):
    def __init__(self):
        self.hashed_files = {}
        self.max_post_process_passes = 3
        self._patterns = ['*.css', '*.js']  # Example patterns for testing

    def _post_process(self, paths, adjustable_paths, hashed_files):
        # Simulate post-processing logic
        for path in adjustable_paths:
            content = paths[path].read()  # Assume paths are file-like objects
            hash_name = self.file_hash(path, content)
            hashed_files[path] = hash_name
            yield path, hash_name, True, False

    def file_hash(self, name, content):
        return hashlib.md5(content).hexdigest()

@pytest.fixture
def setup_files():
    paths = {
        'test.css': ContentFile(b'body { color: red; }'),
        'test.js': ContentFile(b'console.log("Hello World");'),
        'unmatched.txt': ContentFile(b'This will not be processed.'),
    }
    return paths

def test_post_process(setup_files):
    mixin = TestHashedFilesMixin()
    paths = setup_files

    # Test without dry_run
    processed_files = list(mixin.post_process(paths, dry_run=False))
    
    assert len(processed_files) == 2  # Only matched files should be processed
    assert all(isinstance(file, tuple) and len(file) == 3 for file in processed_files)
    
    hashed_files = dict(mixin.hashed_files)
    assert 'test.css' in hashed_files
    assert 'test.js' in hashed_files
    assert 'unmatched.txt' not in hashed_files

    # Test with dry_run
    processed_files_dry_run = list(mixin.post_process(paths, dry_run=True))
    
    assert processed_files_dry_run == []  # No files should be processed

    # Test checking substitutions
    mixin._patterns = ['*.css']  # Update patterns to require adjustment
    processed_files_substitutions = list(mixin.post_process(paths, dry_run=False))
    
    assert len(processed_files_substitutions) > 0  # Should process only CSS files
    assert 'All' in [name for name, _, _ in processed_files_substitutions]