import pytest
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models

class BaseModelAdmin(admin.ModelAdmin):
    model = User

    def get_ordering(self, request):
        return ['username']  # Example ordering for the test

    def get_queryset(self, request):
        qs = self.model._default_manager.get_queryset()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

@pytest.mark.django_db
def test_get_queryset():
    # Create sample users
    User.objects.create_user(username='alice', password='password')
    User.objects.create_user(username='bob', password='password')
    
    admin_instance = BaseModelAdmin(model=User, admin_site=admin.site)
    
    # Test without ordering
    qs = admin_instance.get_queryset(None)
    assert qs.count() == 2
    assert set(user.username for user in qs) == {'alice', 'bob'}

    # Test with ordering applied
    qs = admin_instance.get_queryset(None)
    assert list(qs.values_list('username', flat=True)) == ['alice', 'bob']

    # Create another user to check if ordering works correctly
    User.objects.create_user(username='charlie', password='password')
    
    # Test again with ordering
    qs = admin_instance.get_queryset(None)
    assert list(qs.values_list('username', flat=True)) == ['alice', 'bob', 'charlie']