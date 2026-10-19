import pytest
from django.db.models import JSONField
from django.contrib.auth.models import User
from django.db.models.sql import compiler
from django.db import connection
from your_module_path import HasKeyLookup  # replace 'your_module_path' with the actual module path

@pytest.mark.parametrize("template", [
    "JSON_TYPE(%s, %%s) IS NOT NULL"
])
def test_as_sqlite(template):
    # Instantiate a compiler and connection
    db = connection
    comp = compiler.SQLCompiler(User, db)
    
    # Create an instance of HasKeyLookup
    lookup = HasKeyLookup()
    lookup.logical_operator = 'AND'  # Set the logical operator if needed
    
    # Call the as_sqlite method
    sql = lookup.as_sqlite(comp, db)
    
    # Check the generated SQL
    assert isinstance(sql, tuple)
    assert len(sql) == 2
    assert template in sql[0]  # Check if the template is in the SQL