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
import pytest


class AutoFieldMeta:
    def _subclasses(self):
        return (User,)

    def __instancecheck__(self, instance):
        return isinstance(instance, self._subclasses()) or super().__instancecheck__(instance)


@pytest.fixture
def auto_field_meta():
    return AutoFieldMeta()


def test_instancecheck_with_valid_subclass(auto_field_meta):
    user_instance = User(username='testuser')
    assert auto_field_meta.__instancecheck__(user_instance) is True


def test_instancecheck_with_invalid_class(auto_field_meta):
    class NonUser:
        pass
    
    non_user_instance = NonUser()
    assert auto_field_meta.__instancecheck__(non_user_instance) is False


def test_instancecheck_with_other_subclass(auto_field_meta):
    class CustomUser(User):
        pass
    
    custom_user_instance = CustomUser(username='testcustomuser')
    assert auto_field_meta.__instancecheck__(custom_user_instance) is True


def test_instancecheck_with_super_instance(auto_field_meta):
    assert auto_field_meta.__instancecheck__(User) is False