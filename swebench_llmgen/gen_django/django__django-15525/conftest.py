# django_conftest.py — copy into each gen_django/<instance>/ as conftest.py.
# Configures Django + a migrated in-memory test DB (via pytest-django) so generated tests can
# both import Django internals AND hit the ORM. pytest runs conftest before collection.
import pytest
import django
from django.conf import settings

if not settings.configured:
    settings.configure(
        DEBUG=True,
        DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
        INSTALLED_APPS=[
            "django.contrib.contenttypes",
            "django.contrib.auth",
            "django.contrib.sites",
            "django.contrib.admin",
            "django.contrib.sessions",
            "django.contrib.messages",
        ],
        MIDDLEWARE=[],
        TEMPLATES=[{
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [], "APP_DIRS": True, "OPTIONS": {},
        }],
        USE_TZ=True,
        SECRET_KEY="test",
    )
    django.setup()


@pytest.fixture(autouse=True)
def _db_access(db):
    # give every generated test DB access without needing @pytest.mark.django_db
    pass
