import io
import os
import pytest
from django.http.response import FileResponse


class TestFileResponse:
    @pytest.fixture
    def file_response(self):
        response = FileResponse()
        response.headers = {}
        response.block_size = 1024
        response.as_attachment = False
        return response

    def test_set_headers_seekable_file(self, file_response):
        filelike = io.BytesIO(b'test content')
        filelike.name = 'test.txt'
        file_response.set_headers(filelike)

        assert file_response.headers["Content-Length"] == 12
        assert file_response.headers["Content-Type"] == "application/octet-stream"
        assert "Content-Disposition" not in file_response.headers

    def test_set_headers_non_seekable_file(self, file_response):
        filelike = io.BytesIO(b'test content')
        filelike.name = 'test.txt'
        filelike.seek(0, io.SEEK_END)  # Make it non-seekable.
        file_response.set_headers(filelike)

        assert file_response.headers["Content-Length"] == 12
        assert file_response.headers["Content-Type"] == "application/octet-stream"
        assert "Content-Disposition" not in file_response.headers

    def test_set_headers_with_filename(self, file_response):
        filelike = io.BytesIO(b'test content')
        filelike.name = 'test.txt'        
        file_response.as_attachment = True
        file_response.set_headers(filelike)

        assert file_response.headers["Content-Disposition"] == 'attachment; filename="test.txt"'
    
    def test_set_headers_with_unknown_mimetype(self, file_response):
        filelike = io.BytesIO(b'test content')
        filelike.name = 'unknown.xyz'
        file_response.set_headers(filelike)

        assert file_response.headers["Content-Type"] == "application/octet-stream"

    def test_set_headers_with_existing_file(self, file_response, tmp_path):
        test_file = tmp_path / "test_file.txt"
        test_file.write_text("Content of the test file.")
        
        with open(test_file, 'rb') as filelike:
            file_response.set_headers(filelike)

        assert file_response.headers["Content-Length"] == 30
        assert file_response.headers["Content-Type"] == "application/octet-stream"
        assert "Content-Disposition" not in file_response.headers