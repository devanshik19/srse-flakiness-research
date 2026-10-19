import io
import mimetypes
import os
import pytest
from django.http.response import FileResponse

class MockFile:
    def __init__(self, name, content):
        self.name = name
        self.content = content
        self.position = 0

    def seek(self, offset, whence=0):
        if whence == 0:  # SEEK_SET
            self.position = offset
        elif whence == 1:  # SEEK_CUR
            self.position += offset
        elif whence == 2:  # SEEK_END
            self.position = len(self.content) + offset

    def tell(self):
        return self.position

    def read(self, size=-1):
        if size == -1 or self.position + size > len(self.content):
            size = len(self.content) - self.position
        chunk = self.content[self.position:self.position + size]
        self.position += size
        return chunk

    def getbuffer(self):
        return self.content

@pytest.fixture
def file_response():
    response = FileResponse()
    response.block_size = 8192
    response.headers = {}
    return response

def test_set_headers_with_seekable_file(file_response):
    content = b"Hello, world!"
    mock_file = MockFile("test.txt", content)
    file_response.set_headers(mock_file)

    assert file_response.headers["Content-Length"] == len(content)
    assert file_response.headers["Content-Type"] == "application/octet-stream"
    assert file_response.headers["Content-Disposition"] is None

def test_set_headers_with_non_seekable_file(file_response):
    class NonSeekableMockFile:
        def __init__(self, name, content):
            self.name = name
            self.content = content

        def tell(self):
            return 0

        def read(self, size=-1):
            return self.content

    content = b"Sample content"
    non_seekable_file = NonSeekableMockFile("sample.txt", content)
    file_response.set_headers(non_seekable_file)

    assert file_response.headers["Content-Length"] == len(content)
    assert file_response.headers["Content-Type"] == "application/octet-stream"

def test_set_headers_with_file_not_exists(file_response):
    class MockFileNotExists:
        name = "non_existent_file.txt"

        def tell(self):
            return 0

        def read(self, size=-1):
            return b""

    mock_file = MockFileNotExists()
    file_response.set_headers(mock_file)

    assert "Content-Length" not in file_response.headers
    assert file_response.headers["Content-Type"] == "application/octet-stream"

def test_set_headers_with_filename(file_response):
    content = b"Test file content"
    mock_file = MockFile("test_file.txt", content)
    file_response._no_explicit_content_type = False
    file_response.set_headers(mock_file)

    assert file_response.headers["Content-Length"] == len(content)
    assert file_response.headers["Content-Disposition"] is None

    # Test content type inference
    mimetypes.init()
    mimetypes.add_type("text/plain", ".txt")
    assert file_response.headers["Content-Type"] == "text/plain"