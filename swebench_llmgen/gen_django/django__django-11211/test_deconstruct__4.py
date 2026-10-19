import collections.abc
from django.db.models import Field
from django.contrib.auth.models import User

def test_field_deconstruct():
    # Create an instance of Field with various parameters
    f = Field(verbose_name="Test Field", name="test_field", primary_key=True, max_length=255, unique=True)

    # Call the deconstruct method
    name, path, args, kwargs = f.deconstruct()

    # Assertions to check if the deconstruct method returns the expected values
    assert name == 'test_field'
    assert path == 'django.db.models.fields.Field'  # Adjust based on actual module path in your field subclass if necessary
    assert args == []

    expected_keywords = {
        'verbose_name': 'Test Field',
        'primary_key': True,
        'max_length': 255,
        'unique': True,
    }
    
    # Check if the keywords match the expected ones
    for key, value in expected_keywords.items():
        assert kwargs.get(key, None) == value

    # Check that defaults are omitted
    for key in [
        'blank', 'null', 'db_index', 'default', 'editable',
        'serialize', 'unique_for_date', 'unique_for_month', 
        'unique_for_year', 'choices', 'help_text', 
        'db_column', 'db_tablespace', 'auto_created', 
        'validators', 'error_messages'
    ]:
        assert key not in kwargs