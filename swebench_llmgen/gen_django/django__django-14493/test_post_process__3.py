import pytest
from django.contrib.staticfiles.storage import HashedFilesMixin
from django.contrib.auth.models import User


class TestHashedFilesMixin(HashedFilesMixin):
    def __init__(self):
        self.default_template = ''
        self.max_post_process_passes = 2
        self.patterns = ['*.css', '*.js']
        self.keep_intermediate_files = False
        self.hashed_files = {}

    def _post_process(self, paths, adjustable_paths, hashed_files):
        # Simulated post processing logic for testing
        for path in adjustable_paths:
            content = paths[path].read_text()  # assuming text file for simplification
            file_hash = self.file_hash(path, content)
            hashed_name = f"{path}.{file_hash}"
            hashed_files[path] = hashed_name
            yield path, hashed_name, content, True


@pytest.fixture
def setup_files(tmp_path):
    path1 = tmp_path / 'test1.css'
    path1.write_text('content of test1')
    path2 = tmp_path / 'test2.js'
    path2.write_text('content of test2')
    return {
        str(path1): path1,
        str(path2): path2,
    }


def test_post_process(setup_files):
    mixin = TestHashedFilesMixin()
    mixin._patterns = mixin.patterns

    # Test without dry_run, should process files
    results = list(mixin.post_process(setup_files, dry_run=False))

    assert len(results) == 2
    for original, hashed, content in results:
        assert original in setup_files
        assert isinstance(hashed, str)
        assert content is not None

    # Further asserting if hashed_names are created correctly
    for original, hashed, content in results:
        assert hashed.startswith(original)  # hashed name should start with the original name
        assert hashed != original  # names should be different for cache-busting

    # Test with dry_run, should not process files
    results_dry_run = list(mixin.post_process(setup_files, dry_run=True))
    assert results_dry_run == []