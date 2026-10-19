import pytest
from django.contrib.auth.models import User
from django.contrib.staticfiles.storage import HashedFilesMixin

class TestHashedFilesMixin(HashedFilesMixin):
    def __init__(self):
        self.patterns = ['*.css', '*.js']  # Example patterns
        self.max_post_process_passes = 3
        self.hashed_files = {}

    def _post_process(self, paths, adjustable_paths, hashed_files):
        for path in paths:
            content = paths[path]
            hash_value = self.file_hash(path, content)
            hashed_name = self.hashed_name(path, content, hash_value)
            yield path, hashed_name, True, False

@pytest.fixture
def hashed_files_mixin():
    return TestHashedFilesMixin()

def test_post_process(hashed_files_mixin):
    paths = {
        'styles/style.css': b'some css content',
        'scripts/script.js': b'some js content',
    }

    # Test the function without dry_run
    result = list(hashed_files_mixin.post_process(paths, dry_run=False))

    assert len(result) == 2
    assert result[0][0] == 'styles/style.css'
    assert result[0][1] != 'styles/style.css'  # Ensure the name has changed due to hashing
    assert result[1][0] == 'scripts/script.js'
    assert result[1][1] != 'scripts/script.js'  # Ensure the name has changed due to hashing

def test_post_process_dry_run(hashed_files_mixin):
    paths = {
        'styles/style.css': b'some css content',
        'scripts/script.js': b'some js content',
    }

    # Test the function in dry_run mode
    result = list(hashed_files_mixin.post_process(paths, dry_run=True))

    assert len(result) == 0  # Should return no results in dry run