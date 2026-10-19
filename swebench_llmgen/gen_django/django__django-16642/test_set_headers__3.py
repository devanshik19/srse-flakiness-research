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

    def seek(self, pos, whence=0):
        if whence == io.SEEK_END:
            self.position = len(self.content) + pos
        elif whence == io.SEEK_SET:
            self.position = pos
        else:
            self.position += pos

    def tell(self):
        return self.position

    def read(self, size=-1):
        if size == -1:
            size = len(self.content) - self.position
        if self.position >= len(self.content):
            return b''
        data = self.content[self.position:self.position + size]
        self.position += size
        return data

    @property
    def seekable(self):
        return True

@pytest.mark.parametrize(
    "filename, content, expected_length",
    [
        ("file.txt", b"Hello World", 11),
        ("image.png", b"\x89PNG\r\n\x1a\n", 8),
        ("empty.txt", b"", 0),
    ]
)
def test_set_headers(filename, content, expected_length):
    response = FileResponse()
    mock_file = MockFile(filename, content)
    response.set_headers(mock_file)

    assert response.headers["Content-Length"] == expected_length
    content_type, _ = mimetypes.guess_type(filename)
    assert response.headers["Content-Type"] == (content_type or "application/octet-stream")
    assert response.headers["Content-Disposition"] == f'attachment; filename="{filename}"'