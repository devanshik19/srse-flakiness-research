import pytest
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models

class TestModelAdmin(admin.ModelAdmin):
    model = User
    ordering = ['username']

def test_get_queryset_with_default_ordering():
    admin_instance = TestModelAdmin()
    request = None  # Replace with an actual request object if necessary
    queryset = admin_instance.get_queryset(request)
    assert queryset.count() == User.objects.count()  # Ensure all users are returned
    assert list(queryset) == list(User.objects.order_by('username'))  # Check ordering

def test_get_queryset_without_ordering():
    class NoOrderModelAdmin(admin.ModelAdmin):
        model = User
        ordering = None

    admin_instance = NoOrderModelAdmin()
    request = None
    queryset = admin_instance.get_queryset(request)
    assert queryset.count() == User.objects.count()  # Ensure all users are returned
    assert list(queryset) == list(User.objects.all())  # Check no specific ordering

def test_get_queryset_with_custom_ordering():
    class CustomOrderModelAdmin(admin.ModelAdmin):
        model = User
        ordering = ['-email']  # Ordering by email in descending order

    admin_instance = CustomOrderModelAdmin()
    request = None
    queryset = admin_instance.get_queryset(request)
    assert queryset.count() == User.objects.count()  # Ensure all users are returned
    assert list(queryset) == list(User.objects.order_by('-email'))  # Check custom ordering