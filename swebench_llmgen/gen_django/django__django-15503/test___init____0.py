import pytest
from django.db.models.fields.json import JSONField

def test_jsonfield_init_without_encoder_or_decoder():
    field = JSONField()
    assert field.encoder is None
    assert field.decoder is None

def test_jsonfield_init_with_callable_encoder():
    def custom_encoder(value):
        return json.dumps(value)
    
    field = JSONField(encoder=custom_encoder)
    assert field.encoder == custom_encoder

def test_jsonfield_init_with_callable_decoder():
    def custom_decoder(value):
        return json.loads(value)

    field = JSONField(decoder=custom_decoder)
    assert field.decoder == custom_decoder

def test_jsonfield_init_with_non_callable_encoder():
    with pytest.raises(ValueError, match="The encoder parameter must be a callable object."):
        JSONField(encoder="not_callable")

def test_jsonfield_init_with_non_callable_decoder():
    with pytest.raises(ValueError, match="The decoder parameter must be a callable object."):
        JSONField(decoder="not_callable")