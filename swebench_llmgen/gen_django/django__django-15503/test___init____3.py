import pytest
from django.db.models import Field
from django.contrib.auth.models import User

class JSONField(Field):
    def __init__(self, verbose_name=None, name=None, encoder=None, decoder=None, **kwargs):
        if encoder and not callable(encoder):
            raise ValueError("The encoder parameter must be a callable object.")
        if decoder and not callable(decoder):
            raise ValueError("The decoder parameter must be a callable object.")
        self.encoder = encoder
        self.decoder = decoder
        super().__init__(verbose_name, name, **kwargs)

def test_jsonfield_init():
    # No encoder and decoder
    json_field = JSONField()
    assert json_field.encoder is None
    assert json_field.decoder is None
    
    # With callable encoder and decoder
    json_field = JSONField(encoder=json.dumps, decoder=json.loads)
    assert json_field.encoder is json.dumps
    assert json_field.decoder is json.loads
    
    # With invalid encoder
    with pytest.raises(ValueError, match="The encoder parameter must be a callable object."):
        JSONField(encoder="not_a_callable")
    
    # With invalid decoder
    with pytest.raises(ValueError, match="The decoder parameter must be a callable object."):
        JSONField(decoder="not_a_callable")