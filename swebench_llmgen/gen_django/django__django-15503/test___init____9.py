import pytest
from django.db.models.fields.json import JSONField

def test_jsonfield_init():
    # Test with no parameters
    field = JSONField()
    assert field.encoder is None
    assert field.decoder is None

    # Test with custom encoder and decoder
    def custom_encoder(value):
        return json.dumps(value)

    def custom_decoder(value):
        return json.loads(value)

    field = JSONField(encoder=custom_encoder, decoder=custom_decoder)
    assert field.encoder == custom_encoder
    assert field.decoder == custom_decoder

    # Test invalid encoder
    with pytest.raises(ValueError, match="The encoder parameter must be a callable object."):
        JSONField(encoder="not_callable")

    # Test invalid decoder
    with pytest.raises(ValueError, match="The decoder parameter must be a callable object."):
        JSONField(decoder="not_callable")