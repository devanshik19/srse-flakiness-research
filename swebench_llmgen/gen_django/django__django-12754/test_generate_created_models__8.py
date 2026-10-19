import pytest
from django.db import models
from django.db.migrations.operations import CreateModel, AddField, AlterUniqueTogether
from django.contrib.auth.models import User
from django.db.migrations.autodetector import MigrationAutodetector

class TestMigrationAutodetector:
    
    @pytest.fixture
    def setup_migration_autodetector(self):
        # Setting up old and new states for migration autodetector
        from_state = {
            'models': {
                ('auth', 'user'): User._meta,
            }
        }
        to_state = {
            'models': {
                ('auth', 'user'): User._meta,
                ('auth', 'profile'): models.Model(
                    name='Profile',
                    fields=[
                        ('user', models.OneToOneField(User, on_delete=models.CASCADE)),
                    ],
                    options={'managed': True},
                ),
            }
        }
        od = MigrationAutodetector(from_state, to_state, None)
        return od
    
    def test_generate_created_models(self, setup_migration_autodetector):
        autodetector = setup_migration_autodetector
        autodetector.new_model_keys = {('auth', 'profile')}
        autodetector.old_model_keys = {('auth', 'user')}
        autodetector.old_unmanaged_keys = set()
        autodetector.new_unmanaged_keys = set()
        autodetector.to_state = autodetector.new_apps = to_state

        autodetector.generate_created_models()

        # Assert that CreateModel operation was added
        assert len(autodetector.operations) == 1
        assert isinstance(autodetector.operations[0], CreateModel)
        assert autodetector.operations[0].name == 'Profile'

        # Assert if AddField operation is correctly added for related fields
        field_operations = [op for op in autodetector.operations if isinstance(op, AddField)]
        assert any(op.model_name == 'profile' for op in field_operations)
        assert any(op.name == 'user' for op in field_operations)

        # Testing AlterUniqueTogether operation if exists
        alter_unique_operations = [op for op in autodetector.operations if isinstance(op, AlterUniqueTogether)]
        assert not alter_unique_operations  # Ensure no unique together operations were added