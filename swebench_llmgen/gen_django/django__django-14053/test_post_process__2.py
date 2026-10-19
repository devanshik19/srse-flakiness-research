import hashlib
import os
import pytest
from django.contrib.staticfiles.storage import HashedFilesMixin
from django.contrib.auth.models import User
from django.core.files.base import ContentFile

class TestHashedFilesMixin(HashedFilesMixin):

    def _post_process(self, paths, adjustable_paths, hashed_files):
        for path in paths:
            content = paths[path]
            hashed_name = f"{path}.hashed"  # Simulated hashed filename
            hashed_files[path] = hashed_name
            yield path, hashed_name, True, False

@pytest.fixture
def setup_hashed_files_mixin():
    mixin = TestHashedFilesMixin()
    mixin.max_post_process_passes = 2
    mixin._patterns = ['*.css', '*.js']  # Example patterns for testing.
    mixin.hashed_files = {}
    return mixin

def test_post_process_normal(setup_hashed_files_mixin):
    mixin = setup_hashed_files_mixin
    paths = {
        'style.css': ContentFile(b'some content'),
        'script.js': ContentFile(b'another content'),
    }
    
    result = list(mixin.post_process(paths))
    
    assert len(result) == 2
    assert result[0] == ('style.css', 'style.css.hashed', True)
    assert result[1] == ('script.js', 'script.js.hashed', True)

def test_post_process_dry_run(setup_hashed_files_mixin):
    mixin = setup_hashed_files_mixin
    paths = {
        'style.css': ContentFile(b'some content'),
    }
    
    result = list(mixin.post_process(paths, dry_run=True))
    
    assert result == []

def test_post_process_with_adjustable_paths(setup_hashed_files_mixin):
    mixin = setup_hashed_files_mixin
    paths = {
        'style.css': ContentFile(b'some content'),
        'script.js': ContentFile(b'another content'),
        'image.png': ContentFile(b'some image content'),
    }
    
    # Simulating that 'script.js' is adjustable.
    mixin._patterns = ['*.js']

    result = list(mixin.post_process(paths))
    
    assert len(result) == 2
    assert result[0] == ('script.js', 'script.js.hashed', True)
    assert result[1] == ('All', None, RuntimeError('Max post-process passes exceeded.'))
    
    assert 'script.js' in mixin.hashed_files
    assert mixin.hashed_files['script.js'] == 'script.js.hashed'