import pytest
from django.contrib.admin.sites import AdminSite
from django.http import HttpResponsePermanentRedirect, Http404
from django.urls import resolve, Resolver404
from django.conf import settings
from django.urls import path

@pytest.fixture
def admin_site():
    return AdminSite()

def test_catch_all_view_redirects_when_slash_appended(admin_site, rf):
    settings.APPEND_SLASH = True
    request = rf.get('/fake-url')
    
    # Create a test URL pattern for resolving
    urlpatterns = [
        path('fake-url/', lambda request: HttpResponsePermanentRedirect('/')),
    ]
    
    request.urlconf = urlpatterns
    response = admin_site.catch_all_view(request, 'fake-url')
    
    assert isinstance(response, HttpResponsePermanentRedirect)
    assert response.status_code == 301
    assert response['Location'] == '/fake-url/'

def test_catch_all_view_raises_404_when_no_match(admin_site, rf):
    settings.APPEND_SLASH = True
    request = rf.get('/non-existent-url')
    
    request.urlconf = None  # No URLconf to test resolving
    with pytest.raises(Http404):
        admin_site.catch_all_view(request, 'non-existent-url')

def test_catch_all_view_no_redirect_when_no_append_slash(admin_site, rf):
    settings.APPEND_SLASH = False
    request = rf.get('/fake-url')
    
    # Create a test URL pattern for resolving
    urlpatterns = [
        path('fake-url/', lambda request: HttpResponsePermanentRedirect('/')),
    ]
    
    request.urlconf = urlpatterns
    response = admin_site.catch_all_view(request, 'fake-url')
    
    assert isinstance(response, Http404)  # Should not raise Http404 since it will direct to the correct URL

def test_catch_all_view_redirects_for_should_append_slash(admin_site, rf):
    settings.APPEND_SLASH = True
    request = rf.get('/test-url')

    urlpatterns = [
        path('test-url/', lambda request: HttpResponsePermanentRedirect('/')),
    ]
    
    request.urlconf = urlpatterns

    # Set a custom attribute to match should_append_slash
    match = resolve('/test-url/')
    match.func.should_append_slash = True

    response = admin_site.catch_all_view(request, 'test-url')
    
    assert isinstance(response, HttpResponsePermanentRedirect)
    assert response.status_code == 301
    assert response['Location'] == '/test-url/'