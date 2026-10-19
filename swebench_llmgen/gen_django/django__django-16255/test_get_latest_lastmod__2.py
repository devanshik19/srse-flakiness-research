import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.sitemaps import Sitemap

class TestSitemap(Sitemap):
    lastmod = None
    
    def items(self):
        return [User.objects.first()]

def test_get_latest_lastmod_no_lastmod():
    sitemap = TestSitemap()
    assert sitemap.get_latest_lastmod() is None

def test_get_latest_lastmod_callable_lastmod():
    def lastmod_func(item):
        return item.date_joined

    sitemap = TestSitemap()
    sitemap.lastmod = lastmod_func
    User.objects.create(username='testuser', date_joined=timezone.now())
    assert sitemap.get_latest_lastmod() is not None

def test_get_latest_lastmod_callable_lastmod_type_error():
    def lastmod_func(item):
        return "not_a_date"

    sitemap = TestSitemap()
    sitemap.lastmod = lastmod_func
    User.objects.create(username='testuser', date_joined=timezone.now())
    assert sitemap.get_latest_lastmod() is None

def test_get_latest_lastmod_non_callable_lastmod():
    lastmod_time = timezone.now()
    sitemap = TestSitemap()
    sitemap.lastmod = lastmod_time
    assert sitemap.get_latest_lastmod() == lastmod_time