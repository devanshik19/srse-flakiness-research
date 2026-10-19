import pytest
from django.contrib.staticfiles.storage import HashedFilesMixin
from django.contrib.auth.models import User
from django.core.files.base import ContentFile

class TestHashedFilesMixin(HashedFilesMixin):

    def __init__(self):
        super().__init__()
        self.max_post_process_passes = 2
        self._patterns = ['*.css', '*.js']
        self.hashed_files = {}

    def _post_process(self, paths, adjustable_paths, hashed_files):
        for name in paths:
            content = paths[name]
            hashed_name = self.hashed_name(name, content, name)
            hashed_files[name] = hashed_name
            yield name, hashed_name, True, False

    def hashed_name(self, name, content, filename):
        return f"{name}.hashed"

@pytest.fixture
def setup_hashed_files_mixin():
    return TestHashedFilesMixin()

def test_post_process_without_dry_run(setup_hashed_files_mixin):
    paths = {
        'file1.css': 'body { color: red; }',
        'file2.js': 'console.log("hello world");'
    }
    
    mixin = setup_hashed_files_mixin
    result = list(mixin.post_process(paths, dry_run=False))

    assert len(result) == 4
    assert result[0] == ('file1.css', 'file1.css.hashed', True)
    assert result[1] == ('file2.js', 'file2.js.hashed', True)
    assert mixin.hashed_files['file1.css'] == 'file1.css.hashed'
    assert mixin.hashed_files['file2.js'] == 'file2.js.hashed'

def test_post_process_with_dry_run(setup_hashed_files_mixin):
    paths = {
        'file1.css': 'body { color: red; }',
        'file2.js': 'console.log("hello world");'
    }
    
    mixin = setup_hashed_files_mixin
    result = list(mixin.post_process(paths, dry_run=True))

    assert len(result) == 0
    assert mixin.hashed_files == {}