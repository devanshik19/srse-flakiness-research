import pytest
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from .fields.json import JSONField

def test_jsonfield_init_valid():
    # Valid initialization
    field = JSONField(verbose_name='Test JSON Field', encoder=json.dumps, decoder=json.loads)
    assert field.verbose_name == 'Test JSON Field'
    assert field.encoder == json.dumps
    assert field.decoder == json.loads

def test_jsonfield_init_invalid_encoder():
    # Invalid encoder (not callable)
    with pytest.raises(ValueError, match="The encoder parameter must be a callable object."):
        JSONField(encoder='not_callable')

def test_jsonfield_init_invalid_decoder():
    # Invalid decoder (not callable)
    with pytest.raises(ValueError, match="The decoder parameter must be a callable object."):
        JSONField(decoder='not_callable')