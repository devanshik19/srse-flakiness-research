import pytest
from django.db.backends.postgresql.client import DatabaseClient

class TestDatabaseClient:

    @pytest.fixture(autouse=True)
    def setup_class(self):
        self.client = DatabaseClient()
        self.client.executable_name = "postgres"

    def test_settings_to_cmd_args_env_default_db(self):
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
        assert args == ["postgres", "postgres"]
        assert env is None

    def test_settings_to_cmd_args_env_with_user_and_host(self):
        settings_dict = {
            "OPTIONS": {},
            "HOST": "localhost",
            "PORT": 5432,
            "NAME": "test_db",
            "USER": "test_user",
            "PASSWORD": "test_pass",
        }
        parameters = []
        args, env = self.client.settings_to_cmd_args_env(settings_dict, parameters)
        assert args == ["postgres", "-U", "test_user", "-h", "localhost", "-p", "5432", "test_db"]
        assert env["PGPASSWORD"] == "test_pass"

    def test_settings_to_cmd_args_env_with_ssl_options(self):
        settings_dict = {
            "OPTIONS": {
                "sslmode": "require",
                "sslrootcert": "/path/to/root.crt",
                "sslcert": "/path/to/cert.crt",
                "sslkey": "/path/to/key.key",
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
        assert args == ["postgres", "-U", "test_user", "-h", "localhost", "-p", "5432", "test_db"]
        assert env["PGPASSWORD"] == "test_pass"
        assert env["PGSSLMODE"] == "require"
        assert env["PGSSLROOTCERT"] == "/path/to/root.crt"
        assert env["PGSSLCERT"] == "/path/to/cert.crt"
        assert env["PGSSLKEY"] == "/path/to/key.key"
        assert env["PGPASSFILE"] == "/path/to/passfile"

    def test_settings_to_cmd_args_env_with_service(self):
        settings_dict = {
            "OPTIONS": {},
            "HOST": None,
            "PORT": None,
            "NAME": None,
            "USER": None,
            "PASSWORD": None,
            "SERVICE": "my_service"
        }
        parameters = []
        args, env = self.client.settings_to_cmd_args_env(settings_dict, parameters)
        assert args == ["postgres", "postgres"]
        assert env["PGSERVICE"] == "my_service"