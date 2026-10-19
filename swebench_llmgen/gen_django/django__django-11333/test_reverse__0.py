import pytest
from django.urls import reverse, Resolver404, NoReverseMatch
from django.contrib.auth.models import User
from django.urls import path

# A simple view for testing purposes
from django.http import HttpResponse

def simple_view(request):
    return HttpResponse("Hello, World!")

# Set up URL patterns for the tests
urlpatterns = [
    path('simple/', simple_view, name='simple_view'),
]

# Fixtures to provide URL configuration
@pytest.fixture
def urlconf():
    import sys
    sys.modules['myapp.urls'] = type(sys)('myapp.urls', (), {"urlpatterns": urlpatterns})
    return 'myapp.urls'

def test_reverse_simple_view(urlconf):
    # Test straightforward reverse
    expected_url = '/simple/'
    assert reverse('simple_view', urlconf=urlconf) == expected_url

def test_reverse_with_args(urlconf):
    # Test reverse with arguments
    urlpatterns_with_args = [
        path('user/<int:user_id>/', simple_view, name='user_view'),
    ]
    
    # Update urls for this test
    import sys
    sys.modules['myapp.urls'] = type(sys)('myapp.urls', (), {"urlpatterns": urlpatterns_with_args})
    
    expected_url = '/user/1/'
    assert reverse('user_view', args=[1], urlconf='myapp.urls') == expected_url

def test_reverse_no_reverse_match(urlconf):
    # Test reverse with a non-existent view
    with pytest.raises(NoReverseMatch):
        reverse('non_existent_view', urlconf=urlconf)

def test_reverse_namespacing(urlconf):
    # Test reverse with namespacing
    urlpatterns_with_namespace = [
        path('namespace/simple/', simple_view, name='namespace:simple_view'),
    ]
    
    import sys
    sys.modules['myapp.urls'] = type(sys)('myapp.urls', (), {"urlpatterns": urlpatterns_with_namespace})
    
    expected_url = '/namespace/simple/'
    assert reverse('namespace:simple_view', urlconf='myapp.urls') == expected_url

def test_reverse_raises_no_reverse_match_with_namespace(urlconf):
    # Test reverse with incorrect namespace
    urlpatterns_with_namespace = [
        path('namespace/simple/', simple_view, name='namespace:simple_view'),
    ]
    
    import sys
    sys.modules['myapp.urls'] = type(sys)('myapp.urls', (), {"urlpatterns": urlpatterns_with_namespace})

    with pytest.raises(NoReverseMatch):
        reverse('namespace:non_existent_view', urlconf='myapp.urls')