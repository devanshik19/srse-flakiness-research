import pytest
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User

class UserAdmin(ModelAdmin):
    model = User

def test_model_admin_str():
    user_admin = UserAdmin(model=User, admin_site=None)
    assert str(user_admin) == f"{User._meta.app_label}.UserAdmin"