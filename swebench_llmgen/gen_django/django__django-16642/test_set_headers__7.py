import io
import mimetypes
import os
import pytest
from django.http import FileResponse
from django.utils.http import content_disposition_header

@pytest.fixture
def file_response():
    response = FileResponse()
    response.block_size = 8192
    response.headers = {}
    return response

def test_set_headers_with_seekable_file(file_response):
    file = io.BytesIO(b"Example content")
    file.name = "example.txt"
    file.seekable = lambda: True
    file_response.set_headers(file)
    
    assert file_response.headers["Content-Length"] == len(b"Example content")
    assert file_response.headers["Content-Type"] == "text/plain"
    assert file_response.headers["Content-Disposition"] == content_disposition_header(False, "example.txt")

def test_set_headers_with_non_seekable_file(file_response):
    class NonSeekableFile:
        def __init__(self, content):
            self.content = content
            self.position = 0

        def read(self, size):
            if self.position < len(self.content):
                data = self.content[self.position:self.position + size]
                self.position += size
                return data
            return b""

        def tell(self):
            return self.position
        
        @property
        def name(self):
            return "non_seekable_file.txt"

    file = NonSeekableFile(b"Non-seekable content")
    file_response.set_headers(file)
    
    assert file_response.headers["Content-Length"] == len(b"Non-seekable content")
    assert file_response.headers["Content-Type"] == "text/plain"
    assert file_response.headers["Content-Disposition"] == content_disposition_header(False, "non_seekable_file.txt")

def test_set_headers_with_file_path(file_response, tmp_path):
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("Test file content")
    file = open(test_file, 'rb')
    file_response.set_headers(file)
    file.close()
    
    assert file_response.headers["Content-Length"] == os.path.getsize(test_file)
    assert file_response.headers["Content-Type"] == mimetypes.guess_type(str(test_file))[0]
    assert file_response.headers["Content-Disposition"] == content_disposition_header(False, "test_file.txt")

def test_set_headers_with_unknown_file_type(file_response):
    file = io.BytesIO(b"Unknown file type content")
    file.name = "unknown_file"
    file_response._no_explicit_content_type = True
    file_response.set_headers(file)
    
    assert file_response.headers["Content-Type"] == "application/octet-stream"