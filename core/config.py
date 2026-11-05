from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env",
                                      env_file_encoding="utf-8",
                                      extra="ignore")


class CookieConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="cookie_")
    secret_key: SecretStr
    admin_secret_key: SecretStr


class JWTConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="jwt_")
    key: SecretStr
    algorithm: str


class DBConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="db_")
    user: str
    password: str
    host: str
    port: int
    name: str


class AdminConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="admin_")
    username: str
    password: str