import pytest
from django.contrib.sitemaps import Sitemap
from django.contrib.auth.models import User

class TestSitemap(Sitemap):
    lastmod = None

    def items(self):
        return [User(username='user1', last_login='2023-01-01'), 
                User(username='user2', last_login='2023-01-02')]

def test_get_latest_lastmod_no_lastmod():
    sitemap = TestSitemap()
    assert sitemap.get_latest_lastmod() is None

def test_get_latest_lastmod_callable_lastmod():
    def custom_lastmod(user):
        return user.last_login

    sitemap = TestSitemap()
    sitemap.lastmod = custom_lastmod
    assert sitemap.get_latest_lastmod() == '2023-01-02'

def test_get_latest_lastmod_non_callable_lastmod():
    sitemap = TestSitemap()
    sitemap.lastmod = '2023-01-01'
    assert sitemap.get_latest_lastmod() == '2023-01-01'

def test_get_latest_lastmod_callable_lastmod_type_error():
    def custom_lastmod(user):
        raise TypeError("Error in lastmod function")

    sitemap = TestSitemap()
    sitemap.lastmod = custom_lastmod
    assert sitemap.get_latest_lastmod() is None