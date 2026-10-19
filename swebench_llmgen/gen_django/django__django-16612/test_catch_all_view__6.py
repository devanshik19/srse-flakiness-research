import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.urls import resolve, Resolver404
from django.conf import settings
from django.test import RequestFactory

class TestAdminSite:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.admin_site = AdminSite()
        self.factory = RequestFactory()
        settings.APPEND_SLASH = True
        
        # Add a test URL pattern to test the redirection
        from django.urls import path

        def sample_view(request):
            return HttpResponsePermanentRedirect('/')

        self.admin_site.get_urls = lambda: [
            path('test/', sample_view, name='sample'),
        ]
        self.url = '/test'

    def test_catch_all_view_redirects(self):
        request = self.factory.get(self.url)
        response = self.admin_site.catch_all_view(request, self.url)
        
        assert response.status_code == 301
        assert response['Location'] == 'http://testserver/test/'

    def test_catch_all_view_does_not_redirect_when_not_appending_slash(self):
        settings.APPEND_SLASH = False
        request = self.factory.get(self.url)
        with pytest.raises(Http404):
            self.admin_site.catch_all_view(request, self.url)

    def test_catch_all_view_raises_404_for_non_resolvable_url(self):
        request = self.factory.get('/nonexistent/')
        with pytest.raises(Http404):
            self.admin_site.catch_all_view(request, '/nonexistent/')
    
    def test_catch_all_view_does_not_redirect_if_func_should_not_append_slash(self):
        def non_redirect_view(request):
            return HttpResponsePermanentRedirect('/')

        self.admin_site.get_urls = lambda: [
            path('test/', non_redirect_view, name='sample', func=None)
        ]
        
        request = self.factory.get(self.url)
        response = self.admin_site.catch_all_view(request, self.url)
        
        assert response.status_code == 404  # Should not redirect and raise 404