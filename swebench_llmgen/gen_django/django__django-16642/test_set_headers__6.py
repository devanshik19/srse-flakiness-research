import io
import mimetypes
import os
import pytest
from django.http.response import FileResponse

@pytest.fixture
def file_response():
    response = FileResponse()
    response.block_size = 4096  # Set a default block size
    response.headers = {}
    return response

def test_set_headers_with_seekable_file(file_response):
    file_content = io.BytesIO(b"Test content")
    file_content.name = "test_file.txt"
    
    file_response.set_headers(file_content)

    assert file_response.headers["Content-Length"] == len(file_content.getvalue())
    assert file_response.headers["Content-Type"] == "text/plain"  # Default type 
    assert file_response.headers["Content-Disposition"] == 'inline; filename="test_file.txt"'

def test_set_headers_with_non_seekable_file(file_response):
    class NonSeekableFile:
        def __init__(self, name):
            self.name = name
            self.content = b"Non-seekable content"
        def tell(self):
            return len(self.content)
        def read(self, size=None):
            return self.content
    
    file_content = NonSeekableFile("non_seekable.txt")
    
    file_response.set_headers(file_content)

    assert file_response.headers["Content-Length"] == len(file_content.content)
    assert file_response.headers["Content-Type"] == "application/octet-stream"

def test_set_headers_with_file_path(file_response, tmp_path):
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("File content for testing.")

    with open(file_path, 'rb') as file_content:
        file_response.set_headers(file_content)

    assert file_response.headers["Content-Length"] == os.path.getsize(file_path)
    assert file_response.headers["Content-Type"] == "text/plain"

def test_set_headers_with_missing_file(file_response):
    file_content = io.BytesIO(b"")
    file_content.name = "missing_file.txt"
    os.remove(file_content.name) if os.path.exists(file_content.name) else None
    
    file_response.set_headers(file_content)

    assert file_response.headers["Content-Length"] == 0