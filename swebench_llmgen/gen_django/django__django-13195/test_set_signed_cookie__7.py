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
from django.http import HttpResponseBase

def test_set_signed_cookie():
    response = HttpResponseBase('', content_type='text/html')
    key = 'my_cookie'
    value = 'my_value'
    salt = 'my_salt'
    
    # Call the focal function
    signed_cookie = response.set_signed_cookie(key, value, salt=salt)
    
    # Check if the cookie is set correctly
    assert signed_cookie is not None
    cookie_header = response.cookies[key]
    
    # Verify that the value is signed
    assert cookie_header.value != value
    assert signing.get_cookie_signer(salt=key + salt).unsign(cookie_header.value) == value
    
    # Verify expected parameters
    assert cookie_header['max-age'] == ''
    assert cookie_header['path'] == ''
    assert cookie_header['domain'] == ''
    assert cookie_header['secure'] == False
    assert cookie_header['httponly'] == False
    assert cookie_header['samesite'] == ''