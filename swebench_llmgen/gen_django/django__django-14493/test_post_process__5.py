import pytest
from django.contrib.staticfiles.storage import HashedFilesMixin
from django.contrib.auth.models import User

class TestHashedFilesMixin(HashedFilesMixin):
    _patterns = ['*.js', '*.css']
    max_post_process_passes = 3
    hashed_files = {}

    def _post_process(self, paths, adjustable_paths, hashed_files):
        for path in paths:
            name = path
            content = paths[path]
            hashed_name = f"{name}.hashed"  # Simulate hashed name generation
            yield name, hashed_name, content, False

def test_post_process(monkeypatch):
    mixin = TestHashedFilesMixin()
    
    # Simulating file paths and contents
    paths = {
        'static/js/app.js': 'console.log("app");',
        'static/css/style.css': 'body { background: #fff; }',
        'static/images/logo.png': 'binarydata',
    }
    
    # Test normal processing
    results = list(mixin.post_process(paths, dry_run=False))
    
    assert len(results) == 3
    assert results[0] == ('static/js/app.js', 'static/js/app.js.hashed', 'console.log("app");')
    assert results[1] == ('static/css/style.css', 'static/css/style.css.hashed', 'body { background: #fff; }')
    assert results[2] == ('static/images/logo.png', 'static/images/logo.png.hashed', 'binarydata')

    # Test dry run mode
    results = list(mixin.post_process(paths, dry_run=True))
    assert results == []

    # Check if hashed files were updated
    assert mixin.hashed_files == {}
    
    # Process again to check updates
    list(mixin.post_process(paths, dry_run=False))
    assert len(mixin.hashed_files) == 3
    assert 'static/js/app.js' in mixin.hashed_files
    assert 'static/css/style.css' in mixin.hashed_files
    assert 'static/images/logo.png' in mixin.hashed_files