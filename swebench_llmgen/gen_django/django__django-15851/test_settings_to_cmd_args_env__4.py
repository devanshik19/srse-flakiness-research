import pytest
from django.db.backends.postgresql.client import DatabaseClient

class TestDatabaseClient:

    @pytest.fixture(autouse=True)
    def setup_class(self):
        self.client = DatabaseClient()
        self.client.executable_name = "psql"  # Assuming psql as the executable for testing

    def test_settings_to_cmd_args_env_with_all_params(self):
        settings_dict = {
            "OPTIONS": {
                "passfile": "/path/to/passfile",
                "service": "myservice",
                "sslmode": "require",
                "sslrootcert": "/path/to/sslrootcert",
                "sslcert": "/path/to/sslcert",
                "sslkey": "/path/to/sslkey"
            },
            "HOST": "localhost",
            "PORT": 5432,
            "NAME": "test_db",
            "USER": "test_user",
            "PASSWORD": "test_pass"
        }
        parameters = ["-c", "search_path=public"]

        args, env = self.client.settings_to_cmd_args_env(settings_dict, parameters)

        assert args == [
            "psql",
            "-U", "test_user",
            "-h", "localhost",
            "-p", "5432",
            "test_db",
            "-c", "search_path=public"
        ]
        assert env == {
            "PGPASSWORD": "test_pass",
            "PGSERVICE": "myservice",
            "PGSSLMODE": "require",
            "PGSSLROOTCERT": "/path/to/sslrootcert",
            "PGSSLCERT": "/path/to/sslcert",
            "PGSSLKEY": "/path/to/sslkey",
            "PGPASSFILE": "/path/to/passfile"
        }

    def test_settings_to_cmd_args_env_with_default_db(self):
        settings_dict = {
            "OPTIONS": {},
            "HOST": "localhost",
            "PORT": 5432,
            "USER": "test_user",
            "PASSWORD": "test_pass"
        }
        parameters = []

        args, env = self.client.settings_to_cmd_args_env(settings_dict, parameters)

        assert args == [
            "psql",
            "-U", "test_user",
            "-h", "localhost",
            "-p", "5432",
            "postgres"
        ]
        assert env == {
            "PGPASSWORD": "test_pass"
        }

    def test_settings_to_cmd_args_env_with_service_only(self):
        settings_dict = {
            "OPTIONS": {},
            "SERVICE": "myservice"
        }
        parameters = []

        args, env = self.client.settings_to_cmd_args_env(settings_dict, parameters)

        assert args == [
            "psql",
            "postgres"
        ]
        assert env == {
            "PGSERVICE": "myservice"
        }

    def test_settings_to_cmd_args_env_with_no_params(self):
        settings_dict = {
            "OPTIONS": {},
            "NAME": None,
            "USER": None,
            "PASSWORD": None
        }
        parameters = []

        args, env = self.client.settings_to_cmd_args_env(settings_dict, parameters)

        assert args == [
            "psql",
            "postgres"
        ]
        assert env is None