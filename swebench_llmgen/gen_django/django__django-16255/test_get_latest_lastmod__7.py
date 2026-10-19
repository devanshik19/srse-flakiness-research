import pytest
from django.contrib.sitemaps import Sitemap
from django.contrib.auth.models import User

class TestSitemap(Sitemap):
    def __init__(self):
        self.lastmod = None

    def items(self):
        return [User(username='testuser')]

def test_get_latest_lastmod_no_lastmod():
    sitemap = TestSitemap()
    assert sitemap.get_latest_lastmod() is None

def test_get_latest_lastmod_callable_lastmod():
    sitemap = TestSitemap()
    sitemap.lastmod = lambda item: item.date_joined
    User.objects.create(username='user1', date_joined='2023-01-01')
    User.objects.create(username='user2', date_joined='2023-01-02')

    assert sitemap.get_latest_lastmod() == max(User.objects.all(), key=lambda u: u.date_joined).date_joined

def test_get_latest_lastmod_non_callable_lastmod():
    sitemap = TestSitemap()
    sitemap.lastmod = '2023-01-01'
    assert sitemap.get_latest_lastmod() == '2023-01-01'

def test_get_latest_lastmod_callable_lastmod_type_error():
    sitemap = TestSitemap()
    sitemap.lastmod = lambda item: 'invalid_date'
    User.objects.create(username='user1')

    assert sitemap.get_latest_lastmod() is None