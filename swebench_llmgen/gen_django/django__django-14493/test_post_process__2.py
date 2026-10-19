import pytest
from django.contrib.auth.models import User
from django.contrib.staticfiles.storage import HashedFilesMixin

class TestHashedFilesMixin(HashedFilesMixin):
    def __init__(self):
        self.max_post_process_passes = 2
        self._patterns = ['*.css', '*.js']
        self.hashed_files = {}

    def _post_process(self, paths, adjustable_paths, hashed_files):
        # Simulated post_process functionality for the test
        for path in adjustable_paths:
            content = paths[path]
            hash_value = self.file_hash(path, content)
            hashed_name = f"{os.path.splitext(path)[0]}-{hash_value}.cache"
            hashed_files[hashed_name] = content
            yield path, hashed_name, content, True

    def file_hash(self, name, content):
        return hashlib.md5(content.encode()).hexdigest()

@pytest.fixture
def setup_hashed_files_mixin():
    return TestHashedFilesMixin()

def test_post_process_no_dry_run(setup_hashed_files_mixin):
    mixin = setup_hashed_files_mixin
    paths = {
        'styles.css': 'body { background: #fff; }',
        'script.js': 'console.log("Hello, World!");'
    }

    results = list(mixin.post_process(paths, dry_run=False))

    assert len(results) == 2
    assert results[0] == ('styles.css', 'styles-<hash1>.cache', 'body { background: #fff; }')
    assert results[1] == ('script.js', 'script-<hash2>.cache', 'console.log("Hello, World!");')

def test_post_process_dry_run(setup_hashed_files_mixin):
    mixin = setup_hashed_files_mixin
    paths = {
        'styles.css': 'body { background: #fff; }',
        'script.js': 'console.log("Hello, World!");'
    }

    results = list(mixin.post_process(paths, dry_run=True))

    assert results == []

def test_post_process_exceeds_max_passes(setup_hashed_files_mixin):
    mixin = setup_hashed_files_mixin
    mixin.max_post_process_passes = 1  # Set to 1 to mock failure
    paths = {
        'scripts.js': '<script src="script.js"></script>',
    }

    results = list(mixin.post_process(paths, dry_run=False))

    assert len(results) == 1
    assert results[0] == ('All', None, RuntimeError('Max post-process passes exceeded.'))