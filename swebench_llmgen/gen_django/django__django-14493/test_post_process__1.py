import pytest
from django.contrib.staticfiles.utils import matches_patterns
from django.contrib.staticfiles.storage import HashedFilesMixin
from django.core.files.base import ContentFile
from collections import defaultdict

class TestHashedFilesMixin(HashedFilesMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hashed_files = defaultdict(str)
        self._patterns = ['*.css', '*.js']
        self.max_post_process_passes = 3

    def _post_process(self, paths, adjustable_paths, hashed_files):
        for path in adjustable_paths:
            content = paths[path]
            hash_content = self.file_hash(path, content)
            hashed_name = self.hashed_name(path, content, hash_content)
            hashed_files[hashed_name] = content
            yield path, hashed_name, ContentFile(content), True

    def file_hash(self, name, content):
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    def hashed_name(self, name, content, hash_content):
        return f"{name}-{hash_content}"

@pytest.fixture
def mixin():
    return TestHashedFilesMixin()

def test_post_process_dry_run(mixin):
    paths = {
        'style.css': 'body { background: #fff; }',
        'script.js': 'console.log("Hello World");'
    }
    result = list(mixin.post_process(paths, dry_run=True))
    assert result == []

def test_post_process_normal(mixin):
    paths = {
        'style.css': 'body { background: #fff; }',
        'script.js': 'console.log("Hello World");'
    }
    result = list(mixin.post_process(paths))
    assert len(result) == 2
    assert result[0][1].startswith('style.css-')
    assert result[1][1].startswith('script.js-')
    assert mixin.hashed_files[result[0][1]] == 'body { background: #fff; }'
    assert mixin.hashed_files[result[1][1]] == 'console.log("Hello World");'

def test_post_process_max_passes(mixin):
    mixin.max_post_process_passes = 1  # Set to 1 for testing purposes
    paths = {
        'style.css': 'body { background: url("image.png"); }',
        'script.js': 'console.log("Hello World");'
    }
    result = list(mixin.post_process(paths))
    assert len(result) == 2
    assert result[-1][2] == RuntimeError('Max post-process passes exceeded.')

def test_post_process_no_adjustable_files(mixin):
    paths = {
        'image.png': 'fake_image_data',
    }
    result = list(mixin.post_process(paths))
    assert len(result) == 1
    assert result[0][1] is None
    assert isinstance(result[0][2], ContentFile)