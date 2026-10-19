import pytest
from django.contrib.auth.models import User
from django.db.models import Field

class TestFieldClone:

    def test_clone_creates_new_field_instance(self):
        original_field = Field(
            verbose_name='Test Field',
            name='test_field',
            primary_key=False,
            max_length=100,
            unique=False,
            blank=True,
            null=True,
            db_index=False
        )
        
        cloned_field = original_field.clone()
        
        assert cloned_field is not original_field
        assert cloned_field.verbose_name == original_field.verbose_name
        assert cloned_field.name == original_field.name
        assert cloned_field.primary_key == original_field.primary_key
        assert cloned_field.max_length == original_field.max_length
        assert cloned_field.unique == original_field.unique
        assert cloned_field.blank == original_field.blank
        assert cloned_field.null == original_field.null
        assert cloned_field.db_index == original_field.db_index

    def test_clone_preserves_attributes(self):
        original_field = Field(
            verbose_name='Another Test Field',
            name='another_test_field',
            primary_key=True,
            max_length=255,
            unique=True,
            blank=False,
            null=False,
            db_index=True
        )
        
        cloned_field = original_field.clone()
        
        assert cloned_field.verbose_name == 'Another Test Field'
        assert cloned_field.name == 'another_test_field'
        assert cloned_field.primary_key is True
        assert cloned_field.max_length == 255
        assert cloned_field.unique is True
        assert cloned_field.blank is False
        assert cloned_field.null is False
        assert cloned_field.db_index is True