import sys
import pkgutil
from importlib import import_module, reload
import pytest
from django.apps import apps
from django.contrib.auth.models import User
from django.db.migrations.loader import MigrationLoader
from django.db import connection

def create_migrations(app_label):
    migrations_dir = f"{app_label}/migrations"
    import os
    if not os.path.exists(migrations_dir):
        os.makedirs(migrations_dir)
    with open(os.path.join(migrations_dir, "0001_initial.py"), "w") as f:
        f.write(f"""
from django.db import migrations

class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]
""")

@pytest.fixture
def migration_loader():
    user_app = apps.get_app_config('auth')
    create_migrations(user_app.label)
    loader = MigrationLoader(connection, None, ignore_no_migrations=True, replace_migrations={})
    return loader

def test_load_disk(migration_loader):
    assert not migration_loader.disk_migrations
    assert not migration_loader.unmigrated_apps
    assert not migration_loader.migrated_apps

    migration_loader.load_disk()

    assert ('auth', '0001_initial') in migration_loader.disk_migrations
    assert 'auth' in migration_loader.migrated_apps
    assert not migration_loader.unmigrated_apps

def test_load_disk_no_migrations(migration_loader):
    apps.get_app_config('auth').migrations_module = None
    migration_loader.load_disk()
    
    assert 'auth' in migration_loader.unmigrated_apps
    assert not migration_loader.disk_migrations
    assert 'auth' not in migration_loader.migrated_apps