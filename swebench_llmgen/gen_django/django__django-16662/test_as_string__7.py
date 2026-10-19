import pytest
from django.db import migrations
from django.contrib.auth.models import User
from django.utils.timezone import now
from django import get_version

# Assuming OperationWriter and MIGRATION_HEADER_TEMPLATE, MIGRATION_TEMPLATE are available in the scope, as they are referenced in the function.
from django.db.migrations.writer import MigrationWriter

@pytest.fixture
def migration_with_operations():
    operations = [migrations.CreateModel(
        name='User',
        fields=[
            ('id', migrations.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('username', migrations.CharField(max_length=150, unique=True)),
        ],
    )]
    return migrations.Migration("migration_name", "0001_initial", operations=operations, dependencies=[])

def test_as_string(migration_with_operations):
    writer = MigrationWriter(migration=migration_with_operations, include_header=True)
    result = writer.as_string()
    
    assert "from django.conf import settings" not in result
    assert "from django.db import migrations" in result
    assert "    initial = False" not in result
    assert "replaces = None" not in result
    assert "CreateModel" in result
    assert "# Functions from the following migrations need manual copying." not in result

    # Testing version and timestamp in the header.
    assert f"version = {get_version()}" in result
    assert f"{now().strftime('%Y-%m-%d %H:%M')}" in result

def test_as_string_with_initial(migration_with_operations):
    migration_with_operations.initial = True
    writer = MigrationWriter(migration=migration_with_operations, include_header=True)
    result = writer.as_string()

    assert "    initial = True" in result