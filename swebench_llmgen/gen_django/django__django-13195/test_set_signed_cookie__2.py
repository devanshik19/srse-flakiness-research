import datetime
import json
import mimetypes
import os
import re
import sys
import time
from email.header import Header
from http.client import responses
from urllib.parse import quote, urlparse
from django.conf import settings
from django.core import signals, signing
from django.core.exceptions import DisallowedRedirect
from django.core.serializers.json import DjangoJSONEncoder
from django.http.cookie import SimpleCookie
from django.utils import timezone
from django.utils.encoding import iri_to_uri
from django.utils.http import http_date
from django.utils.regex_helper import _lazy_re_compile
from django.http import HttpResponse
from django.contrib.auth.models import User
import pytest

class HttpResponseBase(HttpResponse):
    def set_signed_cookie(self, key, value, salt='', **kwargs):
        value = signing.get_cookie_signer(salt=key + salt).sign(value)
        return self.set_cookie(key, value, **kwargs)

@pytest.mark.django_db
def test_set_signed_cookie():
    http_response = HttpResponseBase()
    
    # Test params
    key = 'test_cookie'
    value = 'test_value'
    salt = 'test_salt'
    
    # Set the signed cookie
    http_response.set_signed_cookie(key, value, salt=salt)
    
    # Check if the cookie is set correctly
    cookies = http_response.cookies
    assert key in cookies
    assert cookies[key].value != value  # The value should be signed
    assert cookies[key].value == signing.get_cookie_signer(salt=key + salt).sign(value)