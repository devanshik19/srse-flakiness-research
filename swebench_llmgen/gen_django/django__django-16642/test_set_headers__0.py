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

    def read(self, size=None):
        data = self.content[self.position:self.position + size] if size is not None else self.content[self.position:]
        self.position += len(data)
        return data

    def seek(self, offset, whence=0):
        if whence == 0:  # SEEK_SET
            self.position = offset
        elif whence == 1:  # SEEK_CUR
            self.position += offset
        elif whence == 2:  # SEEK_END
            self.position = len(self.content) + offset

    def tell(self):
        return self.position

    @property
    def seekable(self):
        return True

@pytest.fixture
def file_response():
    response = FileResponse()
    response.headers = {}
    response.block_size = 8192
    return response

def test_set_headers_with_seekable_file(file_response):
    content = b"Hello, World!" * 100
    mock_file = MockFile("example.txt", content)
    file_response.set_headers(mock_file)

    assert file_response.headers["Content-Length"] == len(content)
    assert file_response.headers["Content-Type"] == "application/octet-stream"
    assert file_response.headers["Content-Disposition"] == 'attachment; filename="example.txt"'

def test_set_headers_with_non_seekable_file(file_response):
    class NonSeekableFile:
        def __init__(self, content):
            self.content = content
            self.position = 0

        def read(self, size=None):
            data = self.content[self.position:self.position + size] if size is not None else self.content[self.position:]
            self.position += len(data)
            return data

        @property
        def tell(self):
            return self.position

        @property
        def seekable(self):
            return False

    content = b"Non-seekable content" * 10
    non_seekable_file = NonSeekableFile(content)
    non_seekable_file.getbuffer = lambda: non_seekable_file.content
    file_response.set_headers(non_seekable_file)

    assert file_response.headers["Content-Length"] == len(content)
    assert file_response.headers["Content-Type"] == "application/octet-stream"
    assert file_response.headers["Content-Disposition"] == 'attachment; filename=""'

def test_set_headers_with_file_path(file_response, tmp_path):
    test_file_path = tmp_path / "test_file.txt"
    test_file_path.write_text("Sample content.")

    with open(test_file_path, 'rb') as filelike:
        file_response.set_headers(filelike)

    assert file_response.headers["Content-Length"] == os.path.getsize(test_file_path)
    assert file_response.headers["Content-Type"] == "application/octet-stream"
    assert file_response.headers["Content-Disposition"] == f'attachment; filename="{os.path.basename(test_file_path)}"'