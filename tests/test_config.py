import pytest
import os
from unittest.mock import patch

from app.config import Settings, get_settings


class TestSettingsDefaults:
    def test_default_app_name(self):
        s = Settings()
        assert s.APP_NAME == "ComfyGo API"

    def test_default_env(self):
        s = Settings()
        assert s.APP_ENV == "development"

    def test_default_debug(self):
        s = Settings()
        assert s.APP_DEBUG is True

    def test_default_api_prefix(self):
        s = Settings()
        assert s.API_V1_PREFIX == "/api/v1"

    def test_default_jwt_algorithm(self):
        s = Settings()
        assert s.JWT_ALG == "HS256"

    def test_default_jwt_expiry_minutes(self):
        s = Settings()
        assert s.JWT_EXP_MIN == 60

    def test_default_refresh_expiry_days(self):
        s = Settings()
        assert s.JWT_REFRESH_EXP_DAYS == 7

    def test_default_pg_port(self):
        s = Settings()
        assert s.PG_PORT == 5432

    def test_default_log_level(self):
        s = Settings()
        assert s.LOG_LEVEL == "INFO"


class TestSettingsDatabaseUrl:
    def test_database_url_from_parts(self):
        s = Settings()
        url = s.database_url
        assert "postgresql+psycopg2://" in url
        assert s.PG_USER in url
        assert s.PG_HOST in url
        assert str(s.PG_PORT) in url
        assert s.PG_DB in url

    def test_database_url_explicit(self):
        s = Settings(DATABASE_URL="postgres://custom:5432/mydb")
        assert s.database_url == "postgres://custom:5432/mydb"


class TestSettingsProperties:
    def test_is_production_false(self):
        s = Settings(APP_ENV="development")
        assert s.is_production is False

    def test_is_production_true(self):
        s = Settings(APP_ENV="production")
        assert s.is_production is True

    def test_is_production_case_insensitive(self):
        s = Settings(APP_ENV="Production")
        assert s.is_production is True


class TestGetSettings:
    def test_returns_settings_instance(self):
        s = get_settings()
        assert isinstance(s, Settings)
