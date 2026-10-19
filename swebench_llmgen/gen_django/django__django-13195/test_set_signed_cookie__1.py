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

class CustomHttpResponse(HttpResponse):
    def set_signed_cookie(self, key, value, salt='', **kwargs):
        value = signing.get_cookie_signer(salt=key + salt).sign(value)
        return self.set_cookie(key, value, **kwargs)

def test_set_signed_cookie():
    # Testing setting a signed cookie
    response = CustomHttpResponse()
    user = User(username="testuser")
    user.set_password("testpassword")
    user.save()

    # Set a cookie and verify
    key = 'my_cookie'
    value = 'my_value'
    salt = 'my_salt'
    
    response.set_signed_cookie(key, value, salt=salt)

    # Get the signed cookie value directly from the response's cookies dict
    cookie_value = response.cookies[key].value

    # Validate if the value is properly signed
    signer = signing.get_cookie_signer(salt=key + salt)
    assert cookie_value == signer.sign(value)

    # Check if the cookie is present in the response cookies
    assert key in response.cookies
    assert response.cookies[key].value == cookie_value