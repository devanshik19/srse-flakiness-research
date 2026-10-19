import pytest
from django.contrib.auth.models import User
from django.contrib.staticfiles.storage import HashedFilesMixin

class TestHashedFilesMixin(HashedFilesMixin):

    def __init__(self):
        self.max_post_process_passes = 2
        self._patterns = ['*.js', '*.css']
        self.hashed_files = {}

    def _post_process(self, paths, adjustable_paths, hashed_files):
        for path in adjustable_paths:
            if path in paths:
                hashed_name = f"{path}.hashed"
                hashed_files[path] = hashed_name
                yield path, hashed_name, True, False
        yield from []

@pytest.fixture
def mixin():
    return TestHashedFilesMixin()

def test_post_process_no_dry_run(mixin):
    paths = {
        'static/js/script.js': ContentFile(b'console.log("test");'),
        'static/css/style.css': ContentFile(b'body { color: red; }'),
        'static/img/icon.png': ContentFile(b'icon data'),
    }

    # Test with no dry run
    results = list(mixin.post_process(paths, dry_run=False))

    assert len(results) == 3
    assert all(result[1].endswith('.hashed') for result in results)  # check all have hashed name
    assert mixin.hashed_files['static/js/script.js'] == 'static/js/script.js.hashed'
    assert mixin.hashed_files['static/css/style.css'] == 'static/css/style.css.hashed'

def test_post_process_with_dry_run(mixin):
    paths = {
        'static/js/script.js': ContentFile(b'console.log("test");'),
        'static/css/style.css': ContentFile(b'body { color: red; }'),
    }

    # Test with dry run
    results = list(mixin.post_process(paths, dry_run=True))
    
    assert results == []  # should yield nothing in dry run mode
    assert mixin.hashed_files == {}  # should not update hashed_files

def test_post_process_with_substitutions(mixin):
    paths = {
        'static/js/script.js': ContentFile(b'console.log("test");'),
        'static/css/style.css': ContentFile(b'body { color: red; }'),
    }

    # Simulate that the first pass yields substitutes
    mixin._post_process = lambda paths, adjustable_paths, hashed_files: iter([
        ('static/js/script.js', 'static/js/script.js.hashed', True, True),
        ('static/css/style.css', 'static/css/style.css.hashed', True, True)
    ])

    results = list(mixin.post_process(paths, dry_run=False))

    assert len(results) == 2
    assert results[0][1].endswith('.hashed')
    assert results[1][1].endswith('.hashed')
    assert mixin.hashed_files['static/js/script.js'] == 'static/js/script.js.hashed'
    assert mixin.hashed_files['static/css/style.css'] == 'static/css/style.css.hashed'

def test_post_process_exceeds_max_passes(mixin):
    paths = {
        'static/js/script.js': ContentFile(b'console.log("test");'),
    }

    # Simulate that substitutions keep yielding
    mixin.max_post_process_passes = 1  # Set to 1 to trigger runtime error on next call

    mixin._post_process = lambda paths, adjustable_paths, hashed_files: iter([
        ('static/js/script.js', 'static/js/script.js.hashed', True, True)
    ])

    results = list(mixin.post_process(paths, dry_run=False))

    assert len(results) == 1
    assert results[0] == ('All', None, RuntimeError('Max post-process passes exceeded.'))