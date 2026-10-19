import pytest
from django.db.models.fields.json import JSONField

def test_jsonfield_initialization_with_valid_encoder_decoder():
    field = JSONField(encoder=json.dumps, decoder=json.loads)
    assert callable(field.encoder)
    assert callable(field.decoder)

def test_jsonfield_initialization_with_invalid_encoder():
    with pytest.raises(ValueError, match="The encoder parameter must be a callable object."):
        JSONField(encoder="not_a_callable")

def test_jsonfield_initialization_with_invalid_decoder():
    with pytest.raises(ValueError, match="The decoder parameter must be a callable object."):
        JSONField(decoder="not_a_callable")

def test_jsonfield_initialization_with_none_encoder_decoder():
    field = JSONField()
    assert field.encoder is None
    assert field.decoder is None

def test_jsonfield_initialization_with_only_verbose_name():
    field = JSONField(verbose_name="Test JSON Field")
    assert field.verbose_name == "Test JSON Field"

def test_jsonfield_initialization_with_only_name():
    field = JSONField(name="test_json_field")
    assert field.name == "test_json_field"