import pytest
from django.contrib.staticfiles.storage import HashedFilesMixin
from django.contrib.auth.models import User

class TestHashedFilesMixin(HashedFilesMixin):
    def __init__(self):
        self.max_post_process_passes = 1
        self._patterns = ['*.css', '*.js']
        self.hashed_files = {}

    def _post_process(self, paths, adjustable_paths, hashed_files):
        # Sample hash function for testing
        for path in paths:
            content = paths[path].read() if hasattr(paths[path], 'read') else paths[path]
            hashed_name = f"{path.split('.')[0]}-{hashlib.md5(content.encode()).hexdigest()}.{path.split('.')[-1]}"
            hashed_files[path] = hashed_name
            yield path, hashed_name, True, False

def test_post_process():
    mixin = TestHashedFilesMixin()
    
    # Prepare test data
    paths = {
        'style.css': ContentFile('body { color: red; }'),
        'script.js': ContentFile('console.log("Hello World");'),
    }

    # Test with dry_run=False
    result = list(mixin.post_process(paths, dry_run=False))
    assert len(result) == 2
    assert result[0][0] == 'style.css'
    assert result[1][0] == 'script.js'
    assert mixin.hashed_files['style.css'] == 'style-{}.css'.format(hashlib.md5('body { color: red; }'.encode()).hexdigest())
    assert mixin.hashed_files['script.js'] == 'script-{}.js'.format(hashlib.md5('console.log("Hello World");'.encode()).hexdigest())

    # Test with dry_run=True
    result_dry_run = list(mixin.post_process(paths, dry_run=True))
    assert result_dry_run == []

    # Check if hashed_files was populated only in non-dry run
    assert len(mixin.hashed_files) == 2