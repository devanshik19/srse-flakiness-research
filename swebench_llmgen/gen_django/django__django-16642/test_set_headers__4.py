import datetime
import io
import json
import mimetypes
import os
import re
import sys
import time
import warnings
from email.header import Header
from http.client import responses
from urllib.parse import urlparse
from asgiref.sync import async_to_sync, sync_to_async
from django.conf import settings
from django.core import signals, signing
from django.core.exceptions import DisallowedRedirect
from django.core.serializers.json import DjangoJSONEncoder
from django.http.cookie import SimpleCookie
from django.utils import timezone
from django.utils.datastructures import CaseInsensitiveMapping
from django.utils.encoding import iri_to_uri
from django.utils.http import content_disposition_header, http_date
from django.utils.regex_helper import _lazy_re_compile
from django.http import FileResponse

def test_set_headers_for_seekable_file():
    response = FileResponse(open(__file__, 'rb'))
    filelike = io.BytesIO(b'Test content')
    filelike.name = 'test_file.txt'
    response.block_size = 1024
    
    response.set_headers(filelike)
    
    assert response.headers["Content-Length"] == 12  # Length of 'Test content'
    assert response.headers["Content-Type"] == 'text/plain'
    assert response.headers["Content-Disposition"] == 'attachment; filename="test_file.txt"'

def test_set_headers_for_file_with_no_name():
    response = FileResponse(open(__file__, 'rb'))
    filelike = io.BytesIO(b'Test content without name')
    response.block_size = 1024
    
    response.set_headers(filelike)
    
    assert response.headers["Content-Length"] == 27  # Length of 'Test content without name'
    assert response.headers["Content-Type"] == 'application/octet-stream'
    assert "Content-Disposition" not in response.headers

def test_set_headers_for_non_seekable_file():
    response = FileResponse(open(__file__, 'rb'))
    content = b'Test content for non-seekable file'
    filelike = io.BytesIO(content)
    filelike.name = 'non_seekable.txt'
    filelike.seekable = lambda: False  # Simulate non-seekable
    response.block_size = 1024

    response.set_headers(filelike)

    assert response.headers["Content-Length"] == len(content)
    assert response.headers["Content-Type"] == 'application/octet-stream'
    assert response.headers["Content-Disposition"] == 'attachment; filename="non_seekable.txt"'