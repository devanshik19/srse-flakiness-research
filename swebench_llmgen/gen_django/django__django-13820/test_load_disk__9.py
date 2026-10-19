import pkgutil
import sys
from importlib import import_module, reload
from django.apps import apps
from django.conf import settings
from django.db.migrations.loader import MigrationLoader
from django.contrib.auth.models import User

def test_load_disk(migrations):
    loader = MigrationLoader(None, None, True, None)
    
    # Mocking the apps with migrations
    apps.get_app_configs = lambda: [
        apps.AppConfig('auth', 'django.contrib.auth'),
        apps.AppConfig('contenttypes', 'django.contrib.contenttypes'),
    ]
    
    def mock_import_module(module_name):
        if module_name == 'django.contrib.auth.migrations':
            return migrations['auth_migrations']
        elif module_name == 'django.contrib.contenttypes.migrations':
            return migrations['contenttypes_migrations']
        raise ModuleNotFoundError
    
    sys.modules['django.contrib.auth'] = mock_import_module('django.contrib.auth')
    sys.modules['django.contrib.contenttypes'] = mock_import_module('django.contrib.contenttypes')
    
    # Prepare migration modules for testing
    migration_auth = type('Migration', (object,), {})
    migration_contenttypes = type('Migration', (object,), {})
    
    migrations['auth_migrations'] = type('module', (object,), {
        '__path__': ['path/to/migrations'],
        '__file__': 'path/to/migrations/__init__.py',
        'Migration': migration_auth
    })
    
    migrations['contenttypes_migrations'] = type('module', (object,), {
        '__path__': ['path/to/migrations'],
        '__file__': 'path/to/migrations/__init__.py',
        'Migration': migration_contenttypes
    })
    
    loader.load_disk()
    
    assert loader.migrated_apps == {'auth', 'contenttypes'}
    assert (('auth', '0001_initial') in loader.disk_migrations)
    assert (('contenttypes', '0001_initial') in loader.disk_migrations)
    assert loader.unmigrated_apps == set()
    
    # Test case for ModuleNotFoundError
    apps.get_app_configs = lambda: [
        apps.AppConfig('invalid_app', 'invalid_app_label'),
    ]
    
    with pytest.raises(ModuleNotFoundError):
        loader.load_disk()
    
    assert 'invalid_app' in loader.unmigrated_apps