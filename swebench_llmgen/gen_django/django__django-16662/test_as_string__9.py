import pytest
from django.contrib.auth.models import User
from django.db import migrations
from django.db.migrations.writer import MigrationWriter

@pytest.fixture
def sample_migration():
    return migrations.Migration(
        name='SampleMigration',
        app='auth',
        operations=[
            migrations.CreateModel(
                name='Profile',
                fields=[
                    ('id', migrationsAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('user', migrations.ForeignKey(to=User, on_delete=migrations.CASCADE)),
                ]
            )
        ],
        dependencies=[
            ('auth', '0001_initial')
        ],
        replaces=None,
        initial=False,
    )

def test_as_string(sample_migration):
    writer = MigrationWriter(sample_migration, include_header=True)
    output = writer.as_string()

    assert "class Migration" in output
    assert "operations" in output
    assert "dependencies" in output
    assert "    initial = True" not in output  # Since initial is False
    assert "from django.db import migrations" in output
    assert "from django.conf import settings" not in output
    assert "replaces = " not in output  # There is no replaces
    assert "version" in output
    assert "timestamp" in output
    assert "Profile" in output  # Check if our model is referenced