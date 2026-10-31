from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env",
                                      env_file_encoding="utf-8",
                                      extra="ignore")


class CookieConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="cookie_")
    secret_key: str
    admin_secret_key: str


class JWTConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="jwt_")
    key: str
    algorithms: str