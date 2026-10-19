import pytest
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User
from django.db import models


class TestBaseModelAdmin(ModelAdmin):
    model = User


def test_get_queryset_no_ordering():
    admin_instance = TestBaseModelAdmin(User)
    request = None  # Simulating a request; adjust as necessary
    queryset = admin_instance.get_queryset(request)
    assert queryset.count() == User.objects.count()
    assert set(queryset) == set(User.objects.all())


def test_get_queryset_with_ordering():
    admin_instance = TestBaseModelAdmin(User)
    request = None  # Simulating a request; adjust as necessary
    admin_instance.ordering = ['username']
    
    queryset = admin_instance.get_queryset(request)
    assert queryset.count() == User.objects.count()
    assert list(queryset) == list(User.objects.order_by('username'))