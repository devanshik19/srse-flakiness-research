import pytest
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User

class TestBaseModelAdmin(ModelAdmin):
    model = User

def test_get_queryset_with_ordering():
    admin = TestBaseModelAdmin(model=User)
    request = None  # Assuming request can be None for this test

    # Create users to test
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    
    # Check default ordering (no ordering specified)
    queryset = admin.get_queryset(request)
    assert list(queryset) == [user1, user2]

    # Test custom ordering
    admin.ordering = ['-username']
    queryset = admin.get_queryset(request)
    assert list(queryset) == [user2, user1]

def test_get_queryset_empty_model():
    admin = TestBaseModelAdmin(model=User)
    request = None

    # Ensure queryset is empty when there are no users
    queryset = admin.get_queryset(request)
    assert list(queryset) == []