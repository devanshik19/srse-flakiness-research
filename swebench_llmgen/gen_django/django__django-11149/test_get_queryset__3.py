import pytest
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User

@pytest.fixture
def user_model_admin():
    class UserAdmin(ModelAdmin):
        model = User

    return UserAdmin()

def test_get_queryset_orders_by_default(user_model_admin):
    request = None  # Assuming that request is not used in this method
    user_model_admin.ordering = ['username']
    
    queryset = user_model_admin.get_queryset(request)
    
    assert queryset.first().username is not None  # Ensure queryset isn't empty
    assert queryset.order_by('username').exists()

def test_get_queryset_without_ordering(user_model_admin):
    request = None  # Assuming that request is not used in this method
    user_model_admin.ordering = None

    queryset = user_model_admin.get_queryset(request)

    assert queryset.first().username is not None  # Ensure queryset isn't empty
    assert queryset.count() == User.objects.count()  # No ordering should return all instances