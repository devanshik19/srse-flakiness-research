import pytest
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User

class TestBaseModelAdmin(ModelAdmin):
    model = User  # Using User model for testing
    
    def get_ordering(self, request):
        return ['username']  # Example ordering by username

def test_get_queryset():
    admin = TestBaseModelAdmin(User, admin_site=None)
    
    # Create test users
    user1 = User.objects.create_user(username='testuser1', password='password')
    user2 = User.objects.create_user(username='testuser2', password='password')
    
    # Test queryset without ordering
    qs = admin.get_queryset(request=None)
    assert qs.count() == 2
    assert set(qs) == {user1, user2}
    
    # Test queryset with ordering
    ordering = admin.get_ordering(request=None)
    qs = admin.get_queryset(request=None).order_by(*ordering)
    assert list(qs) == [user1, user2]  # Assuming ordering is by username