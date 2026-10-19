import pytest
from django.contrib.auth.models import User
from django.contrib.sitemaps import Sitemap

class TestSitemap(Sitemap):
    lastmod = None

    def items(self):
        return [User(username='testuser')]

def test_get_latest_lastmod_no_lastmod():
    sitemap = TestSitemap()
    assert sitemap.get_latest_lastmod() is None

def test_get_latest_lastmod_callable_lastmod():
    sitemap = TestSitemap()
    sitemap.lastmod = lambda item: item.date_joined
    user = User.objects.create(username='testuser', date_joined='2022-01-01')
    
    assert sitemap.get_latest_lastmod() == user.date_joined

def test_get_latest_lastmod_non_callable_lastmod():
    sitemap = TestSitemap()
    user = User.objects.create(username='testuser', date_joined='2022-01-01')
    sitemap.lastmod = user.date_joined
    
    assert sitemap.get_latest_lastmod() == user.date_joined

def test_get_latest_lastmod_callable_lastmod_type_error():
    sitemap = TestSitemap()
    sitemap.lastmod = lambda item: 'invalid'
    
    with pytest.raises(TypeError):
        sitemap.get_latest_lastmod()