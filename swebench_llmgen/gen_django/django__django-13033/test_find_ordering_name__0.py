import collections
import re
from functools import partial
from itertools import chain
from django.core.exceptions import EmptyResultSet, FieldError
from django.db import DatabaseError, NotSupportedError
from django.db.models.constants import LOOKUP_SEP
from django.db.models.expressions import F, OrderBy, Random, RawSQL, Ref, Value
from django.db.models.functions import Cast
from django.db.models.query_utils import Q, select_related_descend
from django.db.models.sql.constants import (
    CURSOR, GET_ITERATOR_CHUNK_SIZE, MULTI, NO_RESULTS, ORDER_DIR, SINGLE,
)
from django.db.models.sql.query import Query, get_order_dir
from django.db.transaction import TransactionManagementError
from django.utils.functional import cached_property
from django.utils.hashable import make_hashable
from django.utils.regex_helper import _lazy_re_compile
from django.contrib.auth.models import User
from django.db.models import Q as DjangoQ

class TestSQLCompiler:
    
    def setup_method(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.compiler = SQLCompiler(None, None, None)

    def test_find_ordering_name_single_field(self):
        name = 'username'
        opts = User._meta
        result = self.compiler.find_ordering_name(name, opts)

        assert len(result) == 1
        assert isinstance(result[0][0], OrderBy)
        assert result[0][0].expression.name == name
        assert not result[0][1]  # No additional ordering.

    def test_find_ordering_name_multiple_fields(self):
        name = 'username__date_joined'
        opts = User._meta
        result = self.compiler.find_ordering_name(name, opts)

        assert len(result) == 2
        assert isinstance(result[0][0], OrderBy)
        assert result[0][0].expression.name == 'username'
        
        assert isinstance(result[1][0], OrderBy)
        assert result[1][0].expression.name == 'date_joined'
        
    def test_find_ordering_name_with_descending_order(self):
        name = 'username DESC'
        opts = User._meta
        result = self.compiler.find_ordering_name(name, opts)

        assert len(result) == 1
        assert result[0][0].descending is True

    def test_find_ordering_name_infinite_loop(self):
        name = 'username'
        opts = User._meta
        
        # Simulate an infinite loop
        self.compiler.query = collections.namedtuple("Query", ["alias_map"])({0: collections.namedtuple("Alias", ["join_cols"])(['username', 'username'])})
        
        with pytest.raises(FieldError, match='Infinite loop caused by ordering.'):
            self.compiler.find_ordering_name(name, opts, already_seen=set())