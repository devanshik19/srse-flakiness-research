import pytest
from django.db.backends.postgresql.client import DatabaseClient

class TestDatabaseClient:

    @pytest.fixture(autouse=True)
    def setup_class(self):
        self.client = DatabaseClient()
        self.client.executable_name = "psql"

    def test_settings_to_cmd_args_env_with_all_params(self):
        settings_dict = {
            "OPTIONS": {},
            "HOST": "localhost",
            "PORT": 5432,
            "NAME": "test_db",
            "USER": "test_user",
            "PASSWORD": "test_pass",
        }
        parameters = ["--example-parameter"]
        args, env = self.client.settings_to_cmd_args_env(settings_dict, parameters)

        assert args == ["psql", "-U", "test_user", "-h", "localhost", "-p", "5432", "test_db", "--example-parameter"]
        assert env == {"PGPASSWORD": "test_pass"}

    def test_settings_to_cmd_args_env_with_missing_name_and_service(self):
        settings_dict = {
            "OPTIONS": {},
            "HOST": None,
            "PORT": None,
            "NAME": None,
            "USER": None,
            "PASSWORD": None,
        }
        parameters = []
        args, env = self.client.settings_to_cmd_args_env(settings_dict, parameters)

        assert args == ["psql", "postgres"]
        assert env is None

    def test_settings_to_cmd_args_env_with_service(self):
        settings_dict = {
            "OPTIONS": {"service": "myservice"},
            "HOST": "localhost",
            "PORT": 5432,
            "NAME": None,
            "USER": "test_user",
            "PASSWORD": "test_pass",
        }
        parameters = []
        args, env = self.client.settings_to_cmd_args_env(settings_dict, parameters)

        assert args == ["psql", "-U", "test_user", "-h", "localhost", "-p", "5432", "postgres"]
        assert env == {"PGPASSWORD": "test_pass", "PGSERVICE": "myservice"}

    def test_settings_to_cmd_args_env_with_ssl_options(self):
        settings_dict = {
            "OPTIONS": {
                "sslmode": "require",
                "sslrootcert": "/path/to/rootcert",
                "sslcert": "/path/to/cert",
                "sslkey": "/path/to/key",
                "passfile": "/path/to/passfile",
            },
            "HOST": "localhost",
            "PORT": 5432,
            "NAME": "test_db",
            "USER": "test_user",
            "PASSWORD": "test_pass",
        }
        parameters = []
        args, env = self.client.settings_to_cmd_args_env(settings_dict, parameters)

        assert args == ["psql", "-U", "test_user", "-h", "localhost", "-p", "5432", "test_db"]
        assert env == {
            "PGPASSWORD": "test_pass", 
            "PGSSLMODE": "require",
            "PGSSLROOTCERT": "/path/to/rootcert",
            "PGSSLCERT": "/path/to/cert",
            "PGSSLKEY": "/path/to/key",
            "PGPASSFILE": "/path/to/passfile",
        }