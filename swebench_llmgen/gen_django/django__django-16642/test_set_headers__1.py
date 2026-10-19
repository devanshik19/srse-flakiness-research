import io
import mimetypes
import os
import pytest
from django.http import FileResponse

@pytest.fixture
def setup_file_response():
    return FileResponse()

def test_set_headers_with_seekable_file(setup_file_response):
    test_file = io.BytesIO(b'This is a test file.')
    test_file.name = 'test_file.txt'
    setup_file_response.headers = {}
    setup_file_response.block_size = 1024

    setup_file_response.set_headers(test_file)
    
    assert setup_file_response.headers['Content-Length'] == 20
    assert setup_file_response.headers['Content-Type'] == 'text/plain; charset=utf-8'
    assert setup_file_response.headers['Content-Disposition'] == 'attachment; filename="test_file.txt"'

def test_set_headers_with_non_seekable_file(setup_file_response):
    class NonSeekableFile:
        def __init__(self):
            self.name = 'non_seekable_file.txt'
            self.content = b'This is a non-seekable file.'
        
        def tell(self):
            return len(self.content)
        
        def read(self, size=None):
            return self.content
    
    non_seekable_file = NonSeekableFile()
    setup_file_response.headers = {}
    setup_file_response.block_size = 1024

    setup_file_response.set_headers(non_seekable_file)

    assert setup_file_response.headers['Content-Length'] == 28
    assert setup_file_response.headers['Content-Type'] == 'application/octet-stream'
    assert setup_file_response.headers['Content-Disposition'] == 'attachment; filename="non_seekable_file.txt"'

def test_set_headers_with_file_on_disk(setup_file_response, tmp_path):
    test_file_path = tmp_path / 'test_file_on_disk.txt'
    test_file_path.write_text('This is a file on disk.')

    with open(test_file_path, 'rb') as test_file:
        setup_file_response.headers = {}
        setup_file_response.block_size = 1024
        
        setup_file_response.set_headers(test_file)
        
        assert setup_file_response.headers['Content-Length'] == 30
        assert setup_file_response.headers['Content-Type'] == 'text/plain; charset=utf-8'
        assert setup_file_response.headers['Content-Disposition'] == 'attachment; filename="test_file_on_disk.txt"'

def test_set_headers_with_unknown_file_type(setup_file_response):
    filelike = io.BytesIO(b'Some content')
    filelike.name = 'unknown_file.abc'
    setup_file_response.headers = {}
    setup_file_response.block_size = 1024

    setup_file_response.set_headers(filelike)

    assert setup_file_response.headers['Content-Length'] == 12
    assert setup_file_response.headers['Content-Type'] == 'application/octet-stream'
    assert setup_file_response.headers['Content-Disposition'] == 'attachment; filename="unknown_file.abc"'