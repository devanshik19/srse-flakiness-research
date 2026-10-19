import pytest
from django.contrib.auth.models import User
from django.contrib.sitemaps import Sitemap

class TestSitemap(Sitemap):
    lastmod = None

    def items(self):
        return [User.objects.first()]

def test_get_latest_lastmod_without_lastmod():
    sitemap = TestSitemap()
    assert sitemap.get_latest_lastmod() is None

def test_get_latest_lastmod_with_static_lastmod():
    sitemap = TestSitemap()
    sitemap.lastmod = "2023-01-01"
    assert sitemap.get_latest_lastmod() == "2023-01-01"

def test_get_latest_lastmod_with_callable_lastmod():
    def get_lastmod(item):
        return item.date_joined.strftime("%Y-%m-%d") if item else None

    User.objects.create(username='testuser', date_joined='2023-01-01')
    sitemap = TestSitemap()
    sitemap.lastmod = get_lastmod
    
    assert sitemap.get_latest_lastmod() == "2023-01-01"

def test_get_latest_lastmod_with_callable_lastmod_type_error():
    def get_lastmod(item):
        raise TypeError("This is an error")

    User.objects.create(username='testuser', date_joined='2023-01-01')
    sitemap = TestSitemap()
    sitemap.lastmod = get_lastmod
    
    assert sitemap.get_latest_lastmod() is None