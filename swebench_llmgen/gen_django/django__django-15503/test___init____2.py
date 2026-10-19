import pytest
from django.db.models import Field
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class JSONField(Field):
    def __init__(
        self,
        verbose_name=None,
        name=None,
        encoder=None,
        decoder=None,
        **kwargs,
    ):
        if encoder and not callable(encoder):
            raise ValueError("The encoder parameter must be a callable object.")
        if decoder and not callable(decoder):
            raise ValueError("The decoder parameter must be a callable object.")
        self.encoder = encoder
        self.decoder = decoder
        super().__init__(verbose_name, name, **kwargs)

def test_jsonfield_init():
    # Test with valid parameters
    field = JSONField(verbose_name="Test JSONField", encoder=json.dumps, decoder=json.loads)
    assert field.verbose_name == "Test JSONField"
    assert field.encoder == json.dumps
    assert field.decoder == json.loads

    # Test with encoder as non-callable
    with pytest.raises(ValueError, match="The encoder parameter must be a callable object."):
        JSONField(encoder="not_a_function")

    # Test with decoder as non-callable
    with pytest.raises(ValueError, match="The decoder parameter must be a callable object."):
        JSONField(decoder="not_a_function")

    # Test with no encoder and decoder
    field_no_encoder_decoder = JSONField(verbose_name="No Encoder/Decoder")
    assert field_no_encoder_decoder.encoder is None
    assert field_no_encoder_decoder.decoder is None