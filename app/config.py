from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "mysql+pymysql://mysql:mysql@localhost:3306/vocabulary_coach"
    anthropic_api_key: str = ""
    secret_key: str = "dev-secret-key-change-in-production"
    environment: str = "development"
    debug: bool = True

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


settings = Settings()
