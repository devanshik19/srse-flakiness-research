import pytest
from django.db.models.fields.json import JSONField

def test_jsonfield_init_with_valid_encoder_decoder():
    field = JSONField(encoder=json.dumps, decoder=json.loads)
    assert field.encoder == json.dumps
    assert field.decoder == json.loads

def test_jsonfield_init_with_invalid_encoder():
    with pytest.raises(ValueError, match="The encoder parameter must be a callable object."):
        JSONField(encoder="not a callable")

def test_jsonfield_init_with_invalid_decoder():
    with pytest.raises(ValueError, match="The decoder parameter must be a callable object."):
        JSONField(decoder="not a callable")

def test_jsonfield_init_with_no_encoder_decoder():
    field = JSONField()
    assert field.encoder is None
    assert field.decoder is None