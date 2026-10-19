import collections.abc
import copy
import datetime
import decimal
import operator
import uuid
import warnings
from base64 import b64decode, b64encode
from functools import partialmethod, total_ordering
from django import forms
from django.apps import apps
from django.conf import settings
from django.core import checks, exceptions, validators
from django.db import connection, connections, router
from django.db.models.constants import LOOKUP_SEP
from django.db.models.query_utils import DeferredAttribute, RegisterLookupMixin
from django.utils import timezone
from django.utils.datastructures import DictWrapper
from django.utils.dateparse import (
    parse_date, parse_datetime, parse_duration, parse_time,
)
from django.utils.duration import duration_microseconds, duration_string
from django.utils.functional import Promise, cached_property
from django.utils.ipv6 import clean_ipv6_address
from django.utils.itercompat import is_iterable
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User

class AutoFieldMeta:
    def _subclasses(self):
        return (User,)

    def __instancecheck__(self, instance):
        return isinstance(instance, self._subclasses()) or super().__instancecheck__(instance)

    def __subclasscheck__(self, subclass):
        return issubclass(subclass, self._subclasses()) or super().__subclasscheck__(subclass)

def test_instancecheck_on_autofield_meta():
    auto_field_meta = AutoFieldMeta()
    
    # Test with an instance of User
    assert auto_field_meta.__instancecheck__(User()) is True
    
    # Test with a non-subclass instance
    class CustomUser:
        pass
    
    assert auto_field_meta.__instancecheck__(CustomUser()) is False
    
    # Test with a non-related object
    assert auto_field_meta.__instancecheck__(object()) is False
    
    # Test with a subclass of User
    class AdminUser(User):
        pass
    
    assert auto_field_meta.__instancecheck__(AdminUser()) is True