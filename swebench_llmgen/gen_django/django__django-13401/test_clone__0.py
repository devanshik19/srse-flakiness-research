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
from django.db.models import Field


def test_clone():
    # Create an instance of a Field
    original_field = Field(verbose_name="Test Field", name="test_field", primary_key=False)

    # Use the clone method to create a new field instance
    cloned_field = original_field.clone()

    # Assert that the cloned field is an instance of the same class
    assert isinstance(cloned_field, Field)

    # Assert that the cloned field's values match the original field's values
    assert cloned_field.verbose_name == original_field.verbose_name
    assert cloned_field.name == original_field.name
    assert cloned_field.primary_key == original_field.primary_key

    # Assert that they are not the same instance
    assert cloned_field is not original_field

    # Test that the attributes unrelated to name and path are retained
    assert cloned_field.auto_creation_counter == original_field.auto_creation_counter
    assert cloned_field.empty_strings_allowed == original_field.empty_strings_allowed