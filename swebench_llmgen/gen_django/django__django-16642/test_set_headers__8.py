import io
import os
import pytest
from django.http.response import FileResponse
from django.core.files.base import ContentFile

@pytest.fixture
def file_response():
    return FileResponse()

def test_set_headers_with_seekable_filelike(file_response):
    file_content = b'This is a test file.'
    filelike = io.BytesIO(file_content)
    filelike.name = 'test_file.txt'
    file_response.block_size = 1024
    file_response.set_headers(filelike)
    
    assert file_response.headers['Content-Length'] == len(file_content)
    assert file_response.headers['Content-Type'] == 'application/octet-stream'
    assert file_response.headers['Content-Disposition'] == 'attachment; filename="test_file.txt"'

def test_set_headers_with_filelike_with_getbuffer(file_response):
    file_content = b'This file is read from a getbuffer.'
    filelike = io.BytesIO(file_content)
    filelike.name = 'test_file_getbuffer.txt'
    file_response.block_size = 1024
    file_response.set_headers(filelike)
    
    assert file_response.headers['Content-Length'] == len(file_content)
    assert file_response.headers['Content-Type'] == 'application/octet-stream'
    assert file_response.headers['Content-Disposition'] == 'attachment; filename="test_file_getbuffer.txt"'

def test_set_headers_with_existing_file(file_response, tmp_path):
    file_content = b'Existing file content.'
    file_path = tmp_path / 'existing_file.txt'
    with open(file_path, 'wb') as f:
        f.write(file_content)
    
    filelike = open(file_path, 'rb')
    file_response.block_size = 1024
    file_response.set_headers(filelike)
    filelike.close()

    assert file_response.headers['Content-Length'] == os.path.getsize(file_path)
    assert file_response.headers['Content-Type'] == 'application/octet-stream'
    assert file_response.headers['Content-Disposition'] == 'attachment; filename="existing_file.txt"'

def test_set_headers_with_no_filename(file_response):
    filelike = io.BytesIO(b'No filename test.')
    file_response.block_size = 1024
    file_response.set_headers(filelike)

    assert file_response.headers['Content-Length'] == len(b'No filename test.')
    assert file_response.headers['Content-Type'] == 'application/octet-stream'
    assert 'Content-Disposition' not in file_response.headers

def test_set_headers_with_unseekable_filelike(file_response):
    file_content = b'This file is not seekable.'
    filelike = io.BytesIO(file_content)
    filelike.name = 'unseekable_file.txt'
    filelike.seek(0, io.SEEK_END)  # Move to end to make it unseekable from start.
    
    file_response.block_size = 1024
    file_response.set_headers(filelike)

    assert file_response.headers['Content-Length'] == len(file_content)
    assert file_response.headers['Content-Type'] == 'application/octet-stream'
    assert file_response.headers['Content-Disposition'] == 'attachment; filename="unseekable_file.txt"'