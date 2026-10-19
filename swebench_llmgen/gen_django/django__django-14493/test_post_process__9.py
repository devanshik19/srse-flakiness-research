import pytest
from django.contrib.staticfiles.storage import HashedFilesMixin
from django.contrib.auth.models import User

class TestHashedFilesMixin(HashedFilesMixin):
    _patterns = ['*.css', '*.js']
    max_post_process_passes = 2
    hashed_files = {}

    def _post_process(self, paths, adjustable_paths, hashed_files):
        for path in adjustable_paths:
            content = paths[path].read() if isinstance(paths[path], ContentFile) else paths[path]
            hash_value = self.file_hash(path, content)
            hashed_name = f'{path}.{hash_value}'
            hashed_files[hashed_name] = content
            yield path, hashed_name, content, True

def test_post_process(django_user_model):
    mixin = TestHashedFilesMixin()
    
    # Mock paths with ContentFile
    paths = {
        'static/style.css': ContentFile(b'body { background: #fff; }'),
        'static/script.js': ContentFile(b'console.log("Hello World");')
    }
    
    # Test dry_run = True
    result = list(mixin.post_process(paths, dry_run=True))
    assert result == []

    # Test dry_run = False
    result = list(mixin.post_process(paths, dry_run=False))
    
    assert len(result) == 2
    assert result[0][0] == 'static/style.css'
    assert result[1][0] == 'static/script.js'
    assert result[0][1] != 'static/style.css'
    assert result[1][1] != 'static/script.js'
    
    # Check if hashed_files has been updated
    assert 'static/style.css' in mixin.hashed_files
    assert 'static/script.js' in mixin.hashed_files
    
    # Validate that the hash has been computed
    assert mixin.hashed_files[mixin.hashed_files.keys()[0]] == b'body { background: #fff; }'
    assert mixin.hashed_files[mixin.hashed_files.keys()[1]] == b'console.log("Hello World");'