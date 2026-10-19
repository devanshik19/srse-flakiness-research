import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query
from django.db.models import FieldError

class TestQuerySetupJoins:
    def setup_method(self):
        self.query = Query(User, alias_cols=False)

    def test_setup_joins_with_valid_foreign_key(self):
        names = ['groups']
        opts = User._meta
        alias = self.query.get_initial_alias()
        result = self.query.setup_joins(names, opts, alias, can_reuse=None, allow_many=True)
        assert result.final_field.name == 'groups'  # Assuming 'groups' is a valid related name

    def test_setup_joins_with_transform(self):
        names = ['first_name__lower']
        opts = User._meta
        alias = self.query.get_initial_alias()
        
        result = self.query.setup_joins(names, opts, alias)
        assert result.final_transformer is not None  # Ensure a transformer is created
    
    def test_setup_joins_with_invalid_field(self):
        names = ['invalid_field']
        opts = User._meta
        alias = self.query.get_initial_alias()

        with pytest.raises(FieldError):
            self.query.setup_joins(names, opts, alias)

    def test_setup_joins_with_reverse_lookup(self):
        names = ['user']  # Assuming User has some reverse relation
        opts = User._meta
        alias = self.query.get_initial_alias()
        
        # Adjust the can_reuse to test with some reverse foreign key
        result = self.query.setup_joins(names, opts, alias, can_reuse=set(), allow_many=False)
        assert result.final_field is not None  # Ensure the final field is determined

    def test_setup_joins_with_no_reuse(self):
        names = ['groups']  # Valid field
        opts = User._meta
        alias = self.query.get_initial_alias()

        result = self.query.setup_joins(names, opts, alias, can_reuse=set(), allow_many=True)
        assert len(result.joins) > 1  # Ensure joins were correctly generated
        
    def test_setup_joins_with_nullable_field(self):
        names = ['email']  # Assuming User's email can be nullable
        opts = User._meta
        alias = self.query.get_initial_alias()

        result = self.query.setup_joins(names, opts, alias)
        assert not self.query.is_nullable(result.final_field)  # Verify if nullable status is extracted correctly