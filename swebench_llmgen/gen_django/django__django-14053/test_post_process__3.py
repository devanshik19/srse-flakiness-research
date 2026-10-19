import pytest
from django.contrib.staticfiles.storage import HashedFilesMixin
from django.contrib.auth.models import User
from django.core.files.base import ContentFile

class TestHashedFilesMixin(HashedFilesMixin):
    def __init__(self):
        self._patterns = []
        self.max_post_process_passes = 2
        self.hashed_files = {}

    def _post_process(self, paths, adjustable_paths, hashed_files):
        # Simulate a basic hashing process for testing
        for path in paths:
            content = paths[path].read() if isinstance(paths[path], ContentFile) else paths[path]
            file_hash = hashlib.md5(content).hexdigest()
            hashed_name = f"{file_hash}-{path}"
            hashed_files[path] = hashed_name
            yield path, hashed_name, True, False

@pytest.fixture
def hashed_files_mixin():
    return TestHashedFilesMixin()

def test_post_process_with_files(hashed_files_mixin):
    paths = {
        'file1.txt': ContentFile(b'Hello World'),
        'file2.txt': ContentFile(b'Goodbye World'),
    }

    result = list(hashed_files_mixin.post_process(paths, dry_run=False))

    assert len(result) == 2
    assert result[0][0] == 'file1.txt'
    assert result[0][1] != 'file1.txt'
    assert result[1][0] == 'file2.txt'
    assert result[1][1] != 'file2.txt'
    assert hashed_files_mixin.hashed_files['file1.txt'] != 'file1.txt'
    assert hashed_files_mixin.hashed_files['file2.txt'] != 'file2.txt'

def test_post_process_dry_run(hashed_files_mixin):
    paths = {
        'file1.txt': ContentFile(b'Hello World'),
    }

    result = list(hashed_files_mixin.post_process(paths, dry_run=True))
    
    assert result == []
    assert hashed_files_mixin.hashed_files == {}