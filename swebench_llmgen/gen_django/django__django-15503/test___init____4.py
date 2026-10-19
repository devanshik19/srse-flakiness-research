import pytest
from django.db.models.fields.json import JSONField


def test_json_field_initialization_with_valid_encoder_decoder():
    # Test with valid encoder and decoder
    def valid_encoder(value):
        return json.dumps(value)

    def valid_decoder(value):
        return json.loads(value)

    field = JSONField(encoder=valid_encoder, decoder=valid_decoder)
    assert field.encoder is valid_encoder
    assert field.decoder is valid_decoder


def test_json_field_initialization_with_invalid_encoder():
    # Test with invalid encoder (not callable)
    with pytest.raises(ValueError, match="The encoder parameter must be a callable object."):
        JSONField(encoder="not_callable")


def test_json_field_initialization_with_invalid_decoder():
    # Test with invalid decoder (not callable)
    with pytest.raises(ValueError, match="The decoder parameter must be a callable object."):
        JSONField(decoder="not_callable")


def test_json_field_initialization_without_encoder_decoder():
    # Test without encoder and decoder parameters
    field = JSONField()
    assert field.encoder is None
    assert field.decoder is None