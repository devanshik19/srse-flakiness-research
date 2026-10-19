import pytest
import hashlib
from django.contrib.staticfiles.storage import HashedFilesMixin
from django.contrib.auth.models import User
from django.core.files.base import ContentFile

class MockHashedFilesMixin(HashedFilesMixin):
    def __init__(self):
        self.max_post_process_passes = 2
        self._patterns = []
        self.hashed_files = {}

    def _post_process(self, paths, adjustable_paths, hashed_files):
        for path in paths:
            content = paths[path]
            hash_name = self.hashed_name(path, content, None)
            hashed_files[path] = hash_name
            yield path, hash_name, True, False

    def hashed_name(self, name, content, filename):
        return f"{name}.{hashlib.md5(content.encode()).hexdigest()}.css"

@pytest.mark.parametrize("dry_run, expected_output", [
    (True, []),
    (False, [("style.css", "style.css.d41d8cd98f00b204e9800998ecf8427e", True)]),
])
def test_post_process(dry_run, expected_output):
    mixin = MockHashedFilesMixin()
    paths = {
        "style.css": ""
    }
    
    results = list(mixin.post_process(paths, dry_run=dry_run))
    assert results == expected_output
    if not dry_run:
        assert mixin.hashed_files == {"style.css": "style.css.d41d8cd98f00b204e9800998ecf8427e"}