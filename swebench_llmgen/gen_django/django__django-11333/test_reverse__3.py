import pytest
from django.urls import reverse as django_reverse
from django.urls.exceptions import NoReverseMatch
from django.contrib.auth.models import User
from django.urls import path

# Creating a simple view for testing
from django.http import HttpResponse

def test_view(request):
    return HttpResponse("Test View")

# Setting up URLs for the test
urlpatterns = [
    path('test/', test_view, name='test_view'),
]

# Ensure the URLconf is set up correctly for reverse function usage
def test_reverse_function():
    # Register the test urls
    from django.urls import include
    from django.conf import settings
    from django.conf.urls import url

    settings.ROOT_URLCONF = __name__

    # Test valid reverse
    assert django_reverse('test_view') == '/test/'

    # Test reverse with namespace
    urlpatterns_with_ns = [
        path('test/', test_view, name='test_view'),
    ]
    urlpatterns = [
        path('app/', include((urlpatterns_with_ns, 'app'), namespace='app')),
    ]
    
    settings.ROOT_URLCONF = __name__

    assert django_reverse('app:test_view') == '/app/test/'

    # Test reverse with invalid view name
    with pytest.raises(NoReverseMatch):
        django_reverse('non_existent_view')

    # Test using args
    assert django_reverse('test_view', args=[]) == '/test/'

    # Test invalid namespace
    with pytest.raises(NoReverseMatch):
        django_reverse('non_existent_namespace:test_view')

    # Test valid namespace with current_app
    assert django_reverse('app:test_view', current_app='app') == '/app/test/'