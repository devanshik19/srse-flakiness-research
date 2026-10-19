import pytest
from django.contrib.sitemaps import Sitemap
from django.contrib.auth.models import User

class TestSitemap(Sitemap):
    def __init__(self, lastmod=None):
        self.lastmod = lastmod

    def items(self):
        return [User(username='user1', last_login=None), User(username='user2', last_login=None)]

def test_get_latest_lastmod_no_lastmod():
    sitemap = TestSitemap()
    assert sitemap.get_latest_lastmod() is None

def test_get_latest_lastmod_callable():
    def lastmod_func(item):
        return item.last_login

    user1 = User(username='user1', last_login='2023-01-01')
    user2 = User(username='user2', last_login='2023-01-02')
    
    sitemap = TestSitemap(lastmod=lastmod_func)
    sitemap.items = lambda: [user1, user2]

    assert sitemap.get_latest_lastmod() == '2023-01-02'

def test_get_latest_lastmod_callable_type_error():
    def lastmod_func(item):
        return "not a date"

    sitemap = TestSitemap(lastmod=lastmod_func)
    sitemap.items = lambda: [User(username='user1'), User(username='user2')]

    assert sitemap.get_latest_lastmod() is None

def test_get_latest_lastmod_non_callable():
    sitemap = TestSitemap(lastmod='2023-01-01')
    assert sitemap.get_latest_lastmod() == '2023-01-01'