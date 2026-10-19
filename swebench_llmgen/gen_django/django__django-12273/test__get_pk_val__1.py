import pytest
from django.contrib.auth.models import User

class TestModelGetPkVal:
    def test_get_pk_val_with_default_meta(self):
        user = User(username='testuser', password='testpass')
        user.save()
        pk_val = user._get_pk_val()
        assert pk_val == user.pk

    def test_get_pk_val_with_custom_meta(self):
        user = User(username='custommetauser', password='testpass')
        user.save()
        custom_meta = user._meta
        pk_val = user._get_pk_val(custom_meta)
        assert pk_val == user.pk