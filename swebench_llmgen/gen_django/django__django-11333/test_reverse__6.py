import pytest
from django.urls import path, reverse as django_reverse
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured

# Assumed URL configuration for testing
urlpatterns = [
    path('user/<int:id>/', lambda request, id: None, name='user_detail'),
    path('user/<int:id>/edit/', lambda request, id: None, name='user_edit'),
]

@pytest.fixture
def setup_urlconf(settings):
    settings.ROOT_URLCONF = __name__  # Use the current module for testing
    # This allows the Django resolver to find our urlpatterns

def test_reverse_user_detail(setup_urlconf):
    user = User.objects.create(username='testuser')
    expected_url = django_reverse('user_detail', kwargs={'id': user.id})
    assert reverse('user_detail', kwargs={'id': user.id}) == expected_url

def test_reverse_user_edit(setup_urlconf):
    user = User.objects.create(username='testuser')
    expected_url = django_reverse('user_edit', kwargs={'id': user.id})
    assert reverse('user_edit', kwargs={'id': user.id}) == expected_url

def test_reverse_no_ns(setup_urlconf):
    user = User.objects.create(username='testuser')
    expected_url = django_reverse('user_detail', kwargs={'id': user.id})
    assert reverse('user_detail', kwargs={'id': user.id}) == expected_url

def test_reverse_invalid_viewname(setup_urlconf):
    with pytest.raises(NoReverseMatch):
        reverse('non_existent_view')

def test_reverse_namespace(setup_urlconf):
    user = User.objects.create(username='testuser')
    expected_url = django_reverse('user_detail', kwargs={'id': user.id})
    
    # Simulating reverse call with namespace handling
    assert reverse('user_detail', kwargs={'id': user.id}, current_app='app_name') == expected_url