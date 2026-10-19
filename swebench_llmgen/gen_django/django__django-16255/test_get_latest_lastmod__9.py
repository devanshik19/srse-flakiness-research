import pytest
from django.contrib.sitemaps import Sitemap
from django.contrib.auth.models import User


class TestSitemap(Sitemap):
    lastmod = None

    def items(self):
        return []


def test_get_latest_lastmod_no_lastmod():
    sitemap = TestSitemap()
    assert sitemap.get_latest_lastmod() is None


def test_get_latest_lastmod_callable_lastmod():
    def lastmod_func(item):
        return item.last_login

    user1 = User.objects.create_user(username='user1', password='password1', last_login='2023-01-01')
    user2 = User.objects.create_user(username='user2', password='password2', last_login='2023-01-02')

    sitemap = TestSitemap()
    sitemap.lastmod = lastmod_func
    sitemap.items = lambda: [user1, user2]

    assert sitemap.get_latest_lastmod() == user2.last_login


def test_get_latest_lastmod_non_callable_lastmod():
    user = User.objects.create_user(username='user3', password='password3', last_login='2023-01-03')

    sitemap = TestSitemap()
    sitemap.lastmod = user.last_login
    sitemap.items = lambda: [user]

    assert sitemap.get_latest_lastmod() == user.last_login


def test_get_latest_lastmod_type_error_in_callable():
    def lastmod_func_type_error(item):
        return "not a date"

    user = User.objects.create_user(username='user4', password='password4')

    sitemap = TestSitemap()
    sitemap.lastmod = lastmod_func_type_error
    sitemap.items = lambda: [user]

    assert sitemap.get_latest_lastmod() is None