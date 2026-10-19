import pytest
from django.db.backends.postgresql.client import DatabaseClient

class TestDatabaseClient:
    
    @pytest.fixture(autouse=True)
    def setup_class(self):
        self.client = DatabaseClient()
        self.client.executable_name = "psql"

    def test_settings_to_cmd_args_env_with_dbname(self):
        settings = {
            "OPTIONS": {},
            "NAME": "test_db",
            "USER": "test_user",
            "HOST": "localhost",
            "PORT": 5432,
            "PASSWORD": "test_password"
        }
        parameters = []
        args, env = self.client.settings_to_cmd_args_env(settings, parameters)

        assert args == ["psql", "-U", "test_user", "-h", "localhost", "-p", "5432", "test_db"]
        assert env == {"PGPASSWORD": "test_password"}

    def test_settings_to_cmd_args_env_with_service(self):
        settings = {
            "OPTIONS": {},
            "SERVICE": "test_service"
        }
        parameters = []
        args, env = self.client.settings_to_cmd_args_env(settings, parameters)

        assert args == ["psql", "postgres"]
        assert env == {"PGSERVICE": "test_service"}

    def test_settings_to_cmd_args_env_with_ssl_options(self):
        settings = {
            "OPTIONS": {
                "sslmode": "require",
                "sslrootcert": "path/to/sslrootcert",
                "sslcert": "path/to/sslcert",
                "sslkey": "path/to/sslkey",
                "passfile": "path/to/passfile"
            },
            "NAME": "test_db",
            "USER": "test_user"
        }
        parameters = []
        args, env = self.client.settings_to_cmd_args_env(settings, parameters)

        assert args == ["psql", "-U", "test_user", "test_db"]
        assert env == {
            "PGSSLMODE": "require",
            "PGSSLROOTCERT": "path/to/sslrootcert",
            "PGSSLCERT": "path/to/sslcert",
            "PGSSLKEY": "path/to/sslkey",
            "PGPASSFILE": "path/to/passfile"
        }

    def test_settings_to_cmd_args_env_without_dbname_or_service(self):
        settings = {
            "OPTIONS": {}
        }
        parameters = []
        args, env = self.client.settings_to_cmd_args_env(settings, parameters)

        assert args == ["psql", "postgres"]
        assert env is None

    def test_settings_to_cmd_args_env_with_missing_options(self):
        settings = {
            "NAME": "test_db", 
            "USER": "test_user",
            "PASSWORD": "test_password"
        }
        parameters = []
        args, env = self.client.settings_to_cmd_args_env(settings, parameters)

        assert args == ["psql", "-U", "test_user", "test_db"]
        assert env == {"PGPASSWORD": "test_password"}