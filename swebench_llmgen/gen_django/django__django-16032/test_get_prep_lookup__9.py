import warnings
import pytest
from django.db.models import ForeignKey, Model
from django.contrib.auth.models import User
from django.db.models.fields.related_lookups import RelatedIn

class RelatedModel(Model):
    user = ForeignKey(User, on_delete=models.CASCADE)

@pytest.mark.parametrize("rhs_value,expected_rhs", [
    ([1, 2, 3], [1, 2, 3]),  # Test with direct values
    ([], []),  # Test with empty rhs
])
def test_get_prep_lookup_single_col(mocker, rhs_value, expected_rhs):
    mock_lhs = mocker.Mock()
    mock_lhs.output_field.path_infos = [mocker.Mock(target_fields=[mocker.Mock(get_prep_value=lambda v: v)])]
    mock_rhs = mocker.Mock()
    mock_rhs.is_direct_value = lambda: True
    mock_rhs.clear_select_clause = mocker.Mock()
    mock_rhs.add_fields = mocker.Mock()
    
    lookup = RelatedIn()
    lookup.lhs = mock_lhs
    lookup.rhs = rhs_value
    
    result = lookup.get_prep_lookup()
    assert lookup.rhs == expected_rhs
    assert result is not None

def test_get_prep_lookup_non_primary_key(mocker):
    mock_lhs = mocker.Mock()
    mock_lhs.output_field.model = RelatedModel
    mock_lhs.field = mocker.Mock(target_field=mocker.Mock(primary_key=False, name='id'))
    mock_rhs = mocker.Mock()
    mock_rhs.has_select_fields = False
    mock_rhs.clear_select_clause = mocker.Mock()
    mock_rhs.add_fields = mocker.Mock()
    
    lookup = RelatedIn()
    lookup.lhs = mock_lhs
    lookup.rhs = mock_rhs
    
    lookup.get_prep_lookup()
    
    mock_rhs.clear_select_clause.assert_called_once()
    mock_rhs.add_fields.assert_called_once_with(['id'], True)

def test_get_prep_lookup_with_primary_key(mocker):
    mock_lhs = mocker.Mock()
    mock_lhs.output_field.model = RelatedModel
    mock_lhs.output_field.primary_key = True
    mock_lhs.field = mocker.Mock(target_field=mocker.Mock(primary_key=False, name='id'))

    mock_rhs = mocker.Mock()
    mock_rhs.has_select_fields = False
    mock_rhs.clear_select_clause = mocker.Mock()
    mock_rhs.add_fields = mocker.Mock()

    lookup = RelatedIn()
    lookup.lhs = mock_lhs
    lookup.rhs = mock_rhs

    lookup.get_prep_lookup()

    mock_rhs.clear_select_clause.assert_called_once()
    mock_rhs.add_fields.assert_called_once_with(['id'], True)